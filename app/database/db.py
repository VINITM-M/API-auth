
from urllib.parse import quote_plus
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core import config

def get_connection():
    encoded_password = quote_plus(config.password)
    engine = create_engine(
        f"postgresql+psycopg2://{config.user}:{encoded_password}@{config.host}:{config.port}/{config.database}"
    )
    return engine


engine = get_connection()

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

session = SessionLocal()