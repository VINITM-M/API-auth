from fastapi import APIRouter, FastAPI
api_router = APIRouter() 

@api_router.get("/health", tags=["health"])
async def health_check():
    return {"status": "healthy"} 

api_router.include_router(
     
    prefix="/weather",
    tags=["weather"] 
    ) 