
from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field

class APIKeyCreate(BaseModel):
    
    email: EmailStr
    no_of_days_expire: int = Field(gt=0, le=365)  

class APIKeyRead(BaseModel):

    email: EmailStr 