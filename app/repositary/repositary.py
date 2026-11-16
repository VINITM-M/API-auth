from Schemas.api_key import USERS, APIKey
from algorithms.symmetric_encryption_decryption import AESCipher
from database import get_db
import uuid 
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse   


class APIKeyRepository:

    def generating_api_key(self):
        return str(uuid.uuid4()) 

    async def create(self, payload):
        with get_db() as db:
            # Ensure user exists or create automatically
            user = db.query(USERS).filter(USERS.email == payload.email).first()
            if not user:
                user = USERS(email=payload.email)
                try: 
                    db.add(user)
                    db.commit()
                    db.refresh(user) 
                except Exception:
                    db.rollback()
                    user = db.query(USERS).filter(USERS.email == payload.email).first()

            # API key generation 
            apikey_generation = self.generating_api_key()

            # AES algorithm for Symmetric key encryption  
            aes = AESCipher(apikey_generation)
            encrypted_data = aes.encrypt_data()

            # Optional password encryption if provided
            encrypted_password = None
            if getattr(payload, "password", None):
                encrypted_password = AESCipher(payload.password).encrypt_data()

            apikey = APIKey(
                api_key_name=payload.api_key_name,
                api_key_hash=encrypted_data,
                password=encrypted_password,
                user_id=user.id
            )

            try: 
                db.add(apikey) 
                db.commit() 
                db.refresh(apikey)  
            except Exception as e:
                db.rollback()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"API key insertion error: {str(e)}"
                )
                
            return {
                "message": "Key generated successfully", 
                "id": apikey.id, 
                "api_key_name": apikey.api_key_name,
                "key_generation": apikey_generation
            }

    async def inserting_api_password(self, payload):
        with get_db() as db:
            query = db.query(APIKey).filter(APIKey.id == payload.id)
            if getattr(payload, "email", None):
                user = db.query(USERS).filter(USERS.email == payload.email).first()
                if user:
                    query = query.filter(APIKey.user_id == user.id)

            api_key = query.first()
            if not api_key:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="API Key not found"
                )

            aes = AESCipher(payload.password)
            encrypted_password = aes.encrypt_data()
            api_key.password = encrypted_password  

            try: 
                db.commit()
                db.refresh(api_key)
            except Exception as e:
                db.rollback()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Error updating API key password"
                )

            return {"message": "Password updated successfully", "id": api_key.id}

    async def retrival_api_key_with_password(self, payload):
        with get_db() as db:
            api_key = db.query(APIKey).filter(APIKey.id == payload.id).first()
            if not api_key:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="API Key not found"
                )

            # If key has no password protection, directly decrypt and return
            if not api_key.password:
                decrypted_key = AESCipher("").decrypt_data(api_key.api_key_hash)
                return JSONResponse(
                    status_code=status.HTTP_200_OK, 
                    content={
                        "message": "Retrieved Successfully", 
                        "id": api_key.id,
                        "api_key_name": api_key.api_key_name,
                        "API_Key_data": decrypted_key 
                    } 
                )

            try:
                decrypted_password = AESCipher("").decrypt_data(api_key.password)
            except Exception:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to decrypt key password."
                )

            if payload.password != decrypted_password:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Incorrect password for this API key"
                )

            try:
                decrypted_hash = AESCipher("").decrypt_data(api_key.api_key_hash) 
            except Exception:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to decrypt API key."
                )

            return JSONResponse(
                status_code=status.HTTP_200_OK, 
                content={
                    "message": "Retrieved Successfully", 
                    "id": api_key.id,
                    "api_key_name": api_key.api_key_name,
                    "API_Key_data": decrypted_hash 
                } 
            )

    async def get_keys_by_email(self, email: str):
        with get_db() as db:
            user = db.query(USERS).filter(USERS.email == email).first()
            if not user:
                return []
            keys = db.query(APIKey).filter(APIKey.user_id == user.id).all()
            return [
                {
                    "id": k.id,
                    "api_key_name": k.api_key_name,
                    "created_at": k.created_at.isoformat() if k.created_at else None,
                    "last_used_at": k.last_used_at.isoformat() if k.last_used_at else None,
                    "is_active": k.is_active,
                    "has_password": bool(k.password)
                }
                for k in keys
            ]
