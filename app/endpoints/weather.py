from fastapi import APIRouter, Depends, Path, Query
from app.Dependencies.dependicies import get_cache 
from app.services.weather_cache import WeatherCache

router = APIRouter() 

def get_city_key(city: str) -> str:

    city_key = city.lower()


@router.get("/current/{city}")
async def get_current_weather(
    city: str = Path(..., description="City name"), 
    units: Literal["standard", "metric", "imperial"] = Query("metric"),
    weather_cache: WeatherCache = Depends(get_cache),
    weather_client: OpenMeteoClient = Depends(get_weather_service),
    x_api_key: str = Depends(verify_api_key)
    ):

    # Try to get from cache first, passing requested units
    cached_data = await weather_cache.get(city_key, current_date, "current", units)