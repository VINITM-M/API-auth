from fastapi import APIRouter, FastAPI

from endpoints import weather
api_router = APIRouter() 

@api_router.get("/health", tags=["health"])
async def health_check():
    return {"status": "healthy"} 

api_router.include_router(
    weather.router,
    prefix="/weather",
    tags=["weather"] 
    ) 