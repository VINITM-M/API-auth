
from datetime import datetime
from typing import Optional
import httpx
from fastapi import HTTPException
from core.config import API_key
from utils import models

class OpenMeteoClient:

    def __init__(self):

        self.url = "https://api.open-meteo.com/v1/forecast"
        self.geocoding_url = "https://geocoding-api.open-meteo.com/v1/search"
        self._client: Optional[httpx.AsyncClient] = None

    #makes http client object before making the connection pool and reuses it for subsequent requests. This is more efficient than creating a new client for each request.
    @property
    async def client(self) -> httpx.AsyncClient:
        """Get or create HTTP client"""
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(timeout=30.0)
        return self._client

    async def make_request(self, url: str, params: dict) -> dict: 
        try:
            client = await self.client #object client 
            response = await client.get(url, params=params)

            response.raise_for_status()
            return response.json()
        
        except httpx.HTTPError as e:
            if e.response.status_code == 404:
                raise HTTPException(
                    status_code=404,  
                    detail= {
                        "code": "LOCATION_NOT_FOUND",
                        "message": "Location not found in OpenMeteo database",
                        "details": str(e)
                    }
                )

            raise HTTPException(
                status_code=500,
                detail={
                    "code": "WEATHER_API_ERROR",
                    "message": "Error fetching weather data",
                    "details": str(e)
                }
            )

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail={
                    "code": "WEATHER_API_ERROR",
                    "message": "Error connecting to weather service",
                    "details": str(e)
                }
            )

    async def get_current_weather(
            self,
            city: str,
            ) -> dict :

        params = {
            "name": city, 
            "count": 1, 
            "language": "en", 
            "format": "json"
        }

        location = await self.make_request(self.geocoding_url, params)

        results = location.get("results", [])

        if not results:
            raise HTTPException(status_code=404, detail=f"Location not found: {city}")

        latitude = results[0]["latitude"]
        longitude = results[0]["longitude"]

        params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": ",".join([
                "temperature_2m", "relative_humidity_2m", "precipitation",
                "cloud_cover", "pressure_msl", "wind_speed_10m",
                "wind_direction_10m",
            ]),
            "daily": ",".join([
                "temperature_2m_max", "temperature_2m_min", "precipitation_sum",
                "wind_speed_10m_max", "wind_direction_10m_dominant",
            ]),
            "timezone": "auto",
        }

        data = await self.make_request(self.url, params)

        # Extract current data
        current = data["current"]
        daily = data["daily"]

        # Convert values based on requested units

        temp = current["temperature_2m"]  # OpenMeteo returns in Celsius
        temp_min = daily["temperature_2m_min"][0]
        temp_max = daily["temperature_2m_max"][0]
        wind_speed = current["wind_speed_10m"]

        response = models.WeatherResponse(

            date=datetime.now().strftime("%Y-%m-%d"),

            cloud_cover=models.CloudCover(
                afternoon=current["cloud_cover"]
            ),

            humidity=models.Humidity(
                afternoon=current["relative_humidity_2m"]
            ),
            
            precipitation=models.Precipitation(
                total=current["precipitation"]
            ),
            
            temperature=models.Temperature(
                min=temp_min,
                max=temp_max,
                afternoon=temp,
                night=temp,
                evening=temp,
                morning=temp,
            ),
            pressure=models.Pressure(
                afternoon=current["pressure_msl"]
            ),
            wind=models.Wind(
                max=models.WindMax(
                    speed=wind_speed,
                    direction=current["wind_direction_10m"]
                )
            ),
            lat=latitude,
            lon=longitude,
        )

        return response