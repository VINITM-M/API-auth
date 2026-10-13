from sqlalchemy import select
from Schemas.api_key import USERS, APIKey
from database import session


class APIKeyRepository:

    async def create(self, payload) -> APIKey:
        
        users = USERS(

            user_email=payload.email, 
            user_password=payload.password_hash 
        )

        #creating session for users 
        session.add(users)
        session.commit()
        session.refresh(users)

        apikey = APIKey(
            user_api_key_name=payload.api_key_name,  
            user_no_of_days_expire=payload.no_of_days_expire, 
            user_api_key_password=payload.api_key_password 
        )

        #creating session for APIKey 
        session.add(apikey) 
        session.commit() 
        session.refresh(apikey) 


    # async def retrive(self, payload ):
        
    #     stmt = select(ApiKeyCreation.key).where(ApiKeyCreation.user_email == payload.email, 
    #                                             ApiKeyCreation.created_at >= datetime.utcnow() - timedelta(days=no_of_days) ) 

    #     return stmt 
