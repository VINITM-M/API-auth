from fastapi import APIRouter
from Filteration.api_key import APIKeyCreate, APIPassword
from repositary.repositary import APIKeyRepository

router = APIRouter() 

@router.post("",tags=["api-keys"])
async def create_api_key(payload: APIKeyCreate  #it validate the data and filter the data what actually we need especially 
):

    return await APIKeyRepository().create(payload)

@router.post("/password", tags = ["password"]) 
async def password(payload : APIPassword):
    
    return await APIKeyRepository().inserting_api_password(payload)   