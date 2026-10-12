
from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field

class APIKeyCreate(BaseModel):
    
    email: EmailStr
    no_of_days_expire: int = Field(gt=0, le=365)  

class APIKeyRead(BaseModel):

<<<<<<< HEAD
    email: EmailStr
    api_key_name: str 
    no_of_requests: Optional[int] = 10 
    days: int = Field(gt=0, le=365)
    billing_cycle: Optional[str] = "monthly" 
    api_key_password: Optional[str] = None 
    
=======
    email: EmailStr 
    number_of_days: int  
>>>>>>> d0032c58f6a9d34014ee1245014a2281c9b00a85
