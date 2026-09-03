import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

API_key = os.getenv("API_KEY")

class Settings(BaseSettings):

    API_KEY: str = API_key

settings = Settings()