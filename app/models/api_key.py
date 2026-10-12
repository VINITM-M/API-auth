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

# users                api_keys              billing
# ─────────            ─────────             ─────────
# id (PK)              id (PK)               id (PK)
# email                user_id (FK)          user_id (FK)
# password_hash        api_key_hash          api_key_id (FK)
# created_at           api_key_name          plan
# updated_at           created_at            billing_cycle
#                      last_used_at          billing_date
#                      is_active             payment_status
#                      expires_at            payment_date
#                      rate_limit            amount   


from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey 
from sqlalchemy.orm import declarative_base
from db import engine 


Base = declarative_base()

class USERS(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False ) 
    password_hash = Column(String, nullable=False) 
    created_at = Column(DateTime, default=datetime.utcnow) 
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow) 


class APIKey(Base): 
    
    __tablename__ = "api_keys"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False) 
    api_key_name = Column(String, nullable=False) 
    api_key_hash = Column(String, unique=True, index=True, nullable=False) 
    created_at = Column(DateTime, default=datetime.utcnow) 
    last_used_at = Column(DateTime, default=datetime.utcnow) 
    is_active = Column(Boolean, default=True) 
    expires_at = Column(DateTime, nullable=False) 
