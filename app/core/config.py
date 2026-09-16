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
max_requests = os.getenv("APIKEY_AUTH_MAX_REQUESTS")
reset_requests_interval = os.getenv("APIKEY_AUTH_RESET_REQUESTS_INTERVAL")

class Settings(BaseSettings):

    API_KEY: str = API_key

settings = Settings()