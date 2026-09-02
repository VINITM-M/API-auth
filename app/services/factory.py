from app.services.weather_cache import WeatherCache
from app.core.config import settings

_weather_client = None 

def get_weather_client():
    global _weather_cache

    if _weather_cache is None: 
        _weather_cache = WeatherCache(
            redis_host= settings.REDIS_HOST,
            redis_port= settings.REDIS_PORT, 
            redis_db= settings.REDIS_DB, 
            redis_password= settings.REDIS_PASSWORD
        ) 

    return _weather_cache 