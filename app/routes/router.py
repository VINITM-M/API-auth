from fastapi import APIRouter
from endpoints import  api_key

api_router = APIRouter() 

@api_router.get("/health", tags=["health"])
async def health_check():
    return {"status": "healthy"} 


#includes all the routers
 
api_router.include_router(
    api_key.router,
    prefix="/create-api-keys",
    tags=["api-keys"] 
)