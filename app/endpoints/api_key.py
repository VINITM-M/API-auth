from fastapi import APIRouter, FastAPI, Depends
from schemas.api_key import APIKeyCreate
from repositary import APIKeyRepository, APIKeyRead

router = APIRouter() 

@router.post("",tags=["api-keys"])
async def create_api_key(payload: APIKeyCreate  #it validate the data and filter the data what actually we need especially 
):

    create_apikey = await APIKeyRepository().create(payload)

    return {
        "message": "Key generated successfully",
        "key": create_apikey.key,
    }

@router.post("",tags=["api-keys"])
async def retrieve_api_key(payload: APIKeyRead  #it validate the data and filter the data what actually we need especially 
):

    retrieve_apikey = await APIKeyRepository().read(payload)
