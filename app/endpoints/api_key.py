from fastapi import APIRouter, FastAPI, Depends
from schemas.api_key import APIKeyCreate
from repositary import APIKeyRepository

router = APIRouter() 

@router.post("/", tags=["api-keys"])
async def create_api_key(payload: APIKeyCreate  #it validate the data and filter the data what actually we need especially 
):

    apikey = await APIKeyRepository().create(payload)
    return {
        "message": "Key generated successfully",
        "key": apikey.key,
    }