from fastapi import APIRouter
from Filteration.api_key import APIKeyCreate, APIPassword
from repositary.repositary import APIKeyRepository

router = APIRouter() 

@router.post("/create-api-keys",description="Create API keys for users")
async def create_api_key(payload: APIKeyCreate  #it validate the data and filter the data what actually we need especially 
):
    return await APIKeyRepository().create(payload)

@router.post("/password", description="Create API password for users") 
async def password(payload : APIPassword):
    
    return await APIKeyRepository().inserting_api_password(payload)    

@router.post('/retrieve-api-key', description = 'retriving api key') 

async def retrive_api_key(payload):

    return await APIKeyRepository().retrival_api_key_with_password(payload)