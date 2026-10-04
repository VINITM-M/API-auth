
from urllib.parse import quote_plus
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core import config

#config details from cofig.py file to local var to easy use it here

user = config.user 
API_key = config.API_key 
password = config.password
host = config.host
port = config.port
database = config.database
max_requests = config.max_requests
reset_requests_interval = config.reset_requests_interval

def get_connection():
    encoded_password = quote_plus(password)
    engine = create_engine(
        f"postgresql+psycopg2://{user}:{encoded_password}@{host}:{port}/{database}"
    )
    return engine

# ORM session factory — use this to add/query/delete ORM objects
engine = get_connection()
SessionLocal = sessionmaker(bind=engine)