from pydantic import BaseModel, EmailStr

class APIKeyCreate(BaseModel):
    email: EmailStr
    api_key_name: str 

class APIPassword(BaseModel):

    
    email: EmailStr
    id : int  
    password: str 