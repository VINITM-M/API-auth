import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

secret= bytes.fromhex(os.getenv("secret", "").strip()) 
user = os.getenv("user")
password = os.getenv("password")
host = os.getenv("host")
port = os.getenv("port")
database = os.getenv("database")
max_requests = os.getenv("max_requests")
reset_requests_interval = os.getenv("reset_requests_interval")
