from Schemas.api_key import USERS, APIKey
from algorithms.encryption_decryption import AESCipher
from database import session
import uuid 

class APIKeyRepository:

    def generating_api_key(self):
        return str(uuid.uuid4()) 

    async def create(self, payload) -> APIKey:

        print("Payload received:", payload)  # Debugging line to check the payload 

        users = USERS(
            email=payload.email
        )

        apikey_generation = self.generating_api_key()
        
        aes  = AESCipher(apikey_generation)
        encrypted_data = aes.encrypt_data()

        #creating session for users 
        session.add(users)
        session.commit()
        session.refresh(users)

        user = (
            session.query(USERS)
            .filter(USERS.email == payload.email)
            .first()
            )

        apikey = APIKey(
            api_key_name=payload.api_key_name,
            api_key_hash=encrypted_data,
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