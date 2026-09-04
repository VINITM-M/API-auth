from fastapi import APIRouter, FastAPI, Depends
from schemas.api_key import APIKeyCreate
from repositary import APIKeyRepository
from db import get_session
from schemas.helper import serialize_api_key

router = APIRouter() 

@router.post("/create-api-key", tags=["api-keys"]) 
async def create_api_key(
    payload: APIKeyCreate
    ):

    apikey = await APIKeyRepository().create(
        user_id = payload.user_id 
        expires_at = payload.expires_at 
        is_active = payload.is_active 
    )

    return apikey