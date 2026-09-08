
from sqlalchemy import create_engine 
from core import config 

#config details 
user = config.user
password = config.password 
host = config.host 
port = config.port 
database = config.database 

def get_connection():
    engine = create_engine(
        f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
    )
    return engine 