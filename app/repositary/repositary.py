from sqlalchemy import select
from Schemas.api_key import USERS, APIKey
from database import session
import uuid 

class APIKeyRepository:

    def generating_api_key(self):
        return str(uuid.uuid4()) 

    async def create(self, payload) -> APIKey:

        users = USERS(
            email=payload.email
        )

        #creating session for users 
        session.add(users)
        session.commit()
        session.refresh(users)

        user = (
            session.query(USERS)
            .filter(USERS.email == payload.email)
            .first()
        )
        
        apikey_generation = self.generating_api_key()

        apikey = APIKey(
            api_key_name=payload.api_key_name,
            api_key_hash=apikey_generation,
            user_id=user.id
        )

        #creating session for APIKey 
        session.add(apikey) 
        session.commit() 
        session.refresh(apikey) 

        return apikey_generation


    # async def retrive(self, payload ):
        
    #     stmt = select(ApiKeyCreation.key).where(ApiKeyCreation.user_email == payload.email, 
    #                                             ApiKeyCreation.created_at >= datetime.utcnow() - timedelta(days=no_of_days) ) 

    #     return stmt 
