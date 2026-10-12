from datetime import timedelta

from sqlalchemy import select, func
from models.api_key import APIKey
from db import SessionLocal
from models import api_key 
from datetime import timedelta

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