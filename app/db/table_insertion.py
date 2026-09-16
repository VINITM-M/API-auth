from datetime import datetime
from pydantic import BaseModel
from sqlalchemy import Boolean, Column, DateTime, Integer, MetaData, String, Table
from db.db import get_connection

engine = get_connection()

# metadata is function structure the information and properties about table Schema into the db.
# Stores table schema and database structure.
metadata = MetaData()

apikey = Table(
    "apikey_creation",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, nullable=False),
    Column("key", String(64), unique=True, nullable=False),
    Column("created_at", DateTime, nullable=False),
    Column("expires_at", DateTime, nullable=True),
    Column("is_active", Boolean, default=True),
    Column("requests_count", Integer, default=0),
    Column("max_requests", Integer, nullable=True),
    Column("reset_at", DateTime, nullable=True),
)


def table_creation():
    metadata.create_all(engine)
    return apikey


def api_info_table_insert(user_id, key, created_at, expires_at, is_active, requests_count, max_requests, reset_at):

    insert_query = apikey.insert().values(
        user_id=user_id,
        key=key,
        created_at=created_at,
        expires_at=expires_at,
        is_active=is_active,
        requests_count=requests_count,
        max_requests=max_requests,
        reset_at=reset_at,
    )

    with engine.connect() as connection:
        connection.execute(insert_query)
        connection.commit()
