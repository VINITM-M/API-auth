from fastapi import HTTPException, status
from database import get_db
from Schemas.api_key import USERS
from algorithms.hashing import hash_password, verify_password
from Filteration.auth import SignupRequest, LoginRequest


class UserRepository:

    async def signup_user(self, payload: SignupRequest):
        with get_db() as db:
            existing_user = db.query(USERS).filter(USERS.email == payload.email).first()
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Email already registered"
                )

            hashed = hash_password(payload.password)
            new_user = USERS(
                email=payload.email,
                password_hash=hashed,
                first_name=payload.first_name,
                last_name=payload.last_name
            )

            db.add(new_user)
            db.commit()
            db.refresh(new_user)

            return {
                "success": True,
                "message": "User registered successfully",
                "user": {
                    "id": new_user.id,
                    "email": new_user.email,
                    "first_name": new_user.first_name,
                    "last_name": new_user.last_name
                }
            }

    async def login_user(self, payload: LoginRequest):
        with get_db() as db:
            user = db.query(USERS).filter(USERS.email == payload.email).first()
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )

            if not user.password_hash or not verify_password(payload.password, user.password_hash):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid password"
                )

            return {
                "success": True,
                "message": "Login successful",
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name
                }
            }

    async def get_user_profile(self, email: str):
        with get_db() as db:
            user = db.query(USERS).filter(USERS.email == email).first()
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )
            return {
                "id": user.id,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name
            }
