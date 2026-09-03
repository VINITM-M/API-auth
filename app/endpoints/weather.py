from fastapi import APIRouter, Depends, Path
from services.openmeto_client import OpenMeteoClient
from services.factory import get_weather_client 

router = APIRouter() 

@router.get("/current/{city}")
async def get_current_weather(
    city: str = Path(..., description="City name"), 
    weather_client: OpenMeteoClient = Depends(get_weather_client)
    ):
    return await weather_client.get_current_weather(city=city)