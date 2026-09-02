from pydantic_settings import BaseSettings
from typing import Optional 

class Settings(BaseSettings):

    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: Optional[str] = None


settings = Settings()