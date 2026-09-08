import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

API_key = os.getenv("API_KEY")
user = os.getenv("user")
password = os.getenv("password")
host = os.getenv("host")
port = os.getenv("port")
database = os.getenv("database")

class Settings(BaseSettings):

    API_KEY: str = API_key

settings = Settings()