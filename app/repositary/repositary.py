<<<<<<< HEAD
from datetime import timedelta

from sqlalchemy import select, func
from models.api_key import APIKey
from db import SessionLocal
from models import api_key 
from datetime import timedelta
=======
from sqlalchemy import select
from schemas.api_key import APIKey
from db import SessionLocal
from schemas import api_key 
>>>>>>> d0032c58f6a9d34014ee1245014a2281c9b00a85

class APIKeyRepository:

    async def create(self, payload) -> APIKey:
        
        users = Users(

            user_email=payload.email, 
            user_password=payload.password_hash 
        )

        apikey = APIKey(
            user_api_key_name=payload.api_key_name,  
            user_no_of_days_expire=payload.no_of_days_expire, 
            user_api_key_password=payload.api_key_password 
        )

<<<<<<< HEAD
    async def read(self, payload):
        with SessionLocal() as session:
            # Build the base query
            
            stmt = (
                select(api_key)
                .where(api_key.user_email == payload.email)
                .where(api_key.created_at >= func.now() - timedelta(days=payload.days))
            )

            result = session.execute(stmt)
            apikey = result.scalar_one_or_none()

            return apikey
=======
    async def retrive(self, payload ):
        
        stmt = select(ApiKeyCreation.key).where(ApiKeyCreation.user_email == payload.email, 
                                                ApiKeyCreation.created_at >= datetime.utcnow() - timedelta(days=no_of_days) ) 

        return stmt 
>>>>>>> d0032c58f6a9d34014ee1245014a2281c9b00a85
