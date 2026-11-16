from pydantic import BaseModel, EmailStr
from typing import Optional


class APIKeyCreate(BaseModel):
    email: EmailStr
    api_key_name: str
    password: Optional[str] = None


class APIPassword(BaseModel):
    id: int
    password: str
    email: Optional[EmailStr] = None


class APIKeyRetrieve(BaseModel):
    id: int
    password: str
