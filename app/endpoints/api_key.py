from fastapi import APIRouter, Query
from Filteration.api_key import APIKeyCreate, APIPassword, APIKeyRetrieve
from repositary.repositary import APIKeyRepository

router = APIRouter() 


@router.post("/create-api-keys", description="Create API keys for users")
async def create_api_key(payload: APIKeyCreate):
    return await APIKeyRepository().create(payload)


@router.post("/password", description="Set or update protection password for an API key") 
async def password(payload: APIPassword):
    return await APIKeyRepository().inserting_api_password(payload)    


@router.post("/retrieve-api-key", description="Retrieve and decrypt API key with password") 
async def retrieve_api_key(payload: APIPassword):
    return await APIKeyRepository().retrival_api_key_with_password(payload)


@router.get("/user-keys", description="List all API keys belonging to a user")
async def get_user_keys(email: str = Query(..., description="User email")):
    return await APIKeyRepository().get_keys_by_email(email)
