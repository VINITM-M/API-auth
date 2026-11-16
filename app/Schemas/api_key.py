from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey 
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime


Base = declarative_base()


class USERS(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow) 

    # Relationships
    api_keys = relationship("APIKey", back_populates="user", cascade="all, delete-orphan")


class APIKey(Base): 
    __tablename__ = "api_keys"

    id = Column(Integer, primary_key=True, index=True)
    api_key_name = Column(String, nullable=False)
    api_key_hash = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow) 
    last_used_at = Column(DateTime, default=datetime.utcnow) 
    is_active = Column(Boolean, default=True)  
    password = Column(String, nullable=True)  

    # Foreign Key
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False) 

    # Relationships
    user = relationship("USERS", back_populates="api_keys")
