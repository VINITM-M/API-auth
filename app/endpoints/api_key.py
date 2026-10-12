from fastapi import APIRouter, FastAPI, Depends
from Filteration.api_key import APIKeyCreate, APIKeyRead 
from repositary.repositary import APIKeyRepository

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

<<<<<<< HEAD
    retrieve_apikey = await APIKeyRepository().read(payload)

    return { 
        "message": "Key retrieved successfully", 
        "key": retrieve_apikey.key if retrieve_apikey else None, 
    } 
=======
    retrieve_apikey = await APIKeyRepository().retrive(payload)
    
>>>>>>> d0032c58f6a9d34014ee1245014a2281c9b00a85
