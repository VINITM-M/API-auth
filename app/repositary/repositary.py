from Schemas.api_key import USERS, APIKey
from algorithms.encryption_decryption import AESCipher
from database import session
import uuid 
from fastapi import HTTPException, status, JSONResponse 
class APIKeyRepository:

    def generating_api_key(self):
        return str(uuid.uuid4()) 

    async def create(self, payload) -> APIKey:

        users = USERS(
            email=payload.email
        )
        #api key generation 
        apikey_generation = self.generating_api_key()

        #api_key encryption and decryption 
        aes  = AESCipher(apikey_generation)
        encrypted_data = aes.encrypt_data()

        try: 
            #creating session for users 
            session.add(users)
            session.commit()
            session.refresh(users) 
        
        except Exception as e : 
            raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="insertion duplicate mail id "
        )

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

        try: 
            #creating session for APIKey 
            session.add(apikey) 
            session.commit() 
            session.refresh(apikey)  
        
        except Exception as e:
            raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="api key insertion have problems"
                    )
            
        return {
            "message" : "key generate successfully", 
            "id" : apikey.id , 
            "key_generation": apikey_generation
        }

    async def inserting_api_password(self, payload):
        
        user = session.query(USERS).filter(USERS.email == payload.email).first()
        
        api_key = session.query(APIKey).filter(APIKey.user_id == user.id, APIKey.id == payload.id).first()

        #encryption password 
        aes  = AESCipher(payload.password)
        encrypted_password = aes.encrypt_data()
        api_key.password = encrypted_password  

        try: 
            session.commit()
            session.refresh(api_key)
        
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail = "genrating error on password insertion")

        return {"message": "Password updated successfully"} 
    
    async def retrival_api_key_with_password(self, payload):
        
        api_key = session.query( APIKey.password, APIKey.api_key_hash ).filter(APIKey.id == payload.id).first()
        password, api_key_hash = api_key

        decrypted_password  = AESCipher().decrypt(password)
        print("decrypted password: ", decrypted_password)

        try: 
            if payload.passoword == decrypted_password: 

                decrypted_hash = AESCipher().decrypt(api_key_hash) 
                print("decrypted hash: ", decrypted_hash) 

                return JSONResponse(

                    status_code = status.HTTP_201_CREATED, 
                    content = {
                        "message " : "Retrieved Sucessfully", 
                        "API_Key_data" : decrypted_hash 
                    } 
                )

            else:
                return JSONResponse(
                    status_code=401,
                    content={"message": "Created successfully", "data": payload}
                ) 
            
        except Exception as e:
            print("error :", e)  