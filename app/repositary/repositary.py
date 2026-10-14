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

        return {
            "message" : "key generate successfully", 
            "id" : apikey.id , 
            "key_generation": apikey_generation
        }

    async def inserting_api_password(self, payload):
        
        user = session.query(USERS).filter(USERS.email == payload.email).first()
        
        api_key = session.query(APIKey).filter(APIKey.user_id == user.id, APIKey.id == payload.id).first()

        api_key.password = payload.password

        session.commit()
        session.refresh(api_key)

        return {"message": "Password updated successfully"}