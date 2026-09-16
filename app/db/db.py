
from urllib.parse import quote_plus
from sqlalchemy import create_engine
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
        f"mysql+pymysql://{user}:{encoded_password}@{host}:{port}/{database}"
    )
    return engine