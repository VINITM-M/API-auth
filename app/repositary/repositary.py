from sqlalchemy import select
from models.api_key import APIKey
from db import SessionLocal
from models import api_key 

class APIKeyRepository:

    async def create(self, payload) -> APIKey:
        
        apikey = APIKey(
            user_email=payload.email,
            no_of_days_expire=payload.no_of_days_expire 
        )

        # Use ORM session to insert the apikey into the database
        with SessionLocal() as session:
            session.add(apikey)
            session.commit()
            session.refresh(apikey)  # populate server-generated fields like id
        
        return apikey 

    async def read(self, payload):

        with SessionLocal() as session:
            
            stmt = select(api_key).where(
                api_key.user_email == payload.email
            )

            result = session.execute(stmt)

            apikey = result.scalar_one_or_none()

            return apikey