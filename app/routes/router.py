from fastapi import APIRouter
from endpoints import api_key, auth

api_router = APIRouter() 


@api_router.get("/health", tags=["Health"])
async def health_check():
    return {"status": "healthy"} 


# Include authentication router (/api/auth/...)
api_router.include_router(
    auth.router
)

# Include API key router (/api/create-api-keys, /api/password, /api/retrieve-api-key, /api/user-keys)
api_router.include_router(
    api_key.router,
    tags=["Manage Keys"] 
)
