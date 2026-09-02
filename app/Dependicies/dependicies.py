from fastapi import HTTPException, Header, Depends
from app.services.factory import get_weather_cache

async def get_cache():
    cache = get_weather_cache()
    try:
        yield cache
    finally:
        await cache.close()