"""
Here, the file speaks about SQL Alchemy ORM.

SQL Alchemy is a toolkit of Python database.

ORM is the part of SQL Alchemy, it's the higher level of SQL Alchemy. By default,
execution of this goes through SQL Core.
SQLAlchemy Core is another part, where the users write low level SQL queries
(insert, delete, etc.).

Currently using the ORM layer 2.0, which internally uses SQLAlchemy Core to generate
and execute SQL. Combining all these, we call it the ORM layer.

Below code speaks about SQLAlchemy ORM only.
It maps Python objects into SQL database tables and columns.

TABLE MAP  ("1 ──< N" means "one has many")

    plans 1 ──< N subscriptions N >── 1 user_accounts 1 ──< N apikeys
                       1
                       │
                       ^
                       N
                    payment   
"""


from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey 
from sqlalchemy.orm import declarative_base, relationship

from database.db import engine

import uuid
from datetime import datetime


Base = declarative_base()

class USERS(Base):
    __tablename__ = "users"

    #primary Key 
    id = Column(Integer, primary_key=True, index=True)

    email = Column(String, unique=True, index=True, nullable=False ) 
    password_hash = Column(String, nullable=False) 
    created_at = Column(DateTime, default=datetime.utcnow) 
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    #define relationship 
    api_key_id = relationship("APIKey", back_populates="user")


class APIKey(Base): 
    
    __tablename__ = "api_keys"

    id = Column(Integer, primary_key=True, index=True)
    api_key_name = Column(String)
    api_key_hash = Column(String, default=lambda: str(uuid.uuid4()), unique=True, index=True, nullable=False) 
    created_at = Column(DateTime, default=datetime.utcnow) 
    last_used_at = Column(DateTime, default=datetime.utcnow) 
    is_active = Column(Boolean, default=True) 
    expires_at = Column(DateTime, nullable=False) 

    #Foreign Key Establishment
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False) 

    #define relationship 
    user = relationship("USERS", back_populates = 'api_key_id')

# Create all tables
Base.metadata.create_all(engine)