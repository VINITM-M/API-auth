from sqlalchemy import select
from schemas.api_key import APIKey
from db import SessionLocal
from schemas import api_key 

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

    async def retrive(self, payload ):
        
        stmt = select(ApiKeyCreation.key).where(ApiKeyCreation.user_email == payload.email, 
                                                ApiKeyCreation.created_at >= datetime.utcnow() - timedelta(days=no_of_days) ) 

        return stmt 