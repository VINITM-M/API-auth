"""Database package initialization."""

from sqlalchemy import text
from database.db import get_connection, session, engine, get_db


def init_db():
    """Create application tables at startup and ensure required columns exist."""
    from Schemas.api_key import Base
    
    # Create tables if not exist
    Base.metadata.create_all(engine)

    # Ensure required columns exist for existing tables (idempotent migrations)
    with engine.begin() as conn:
        conn.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS password_hash VARCHAR;"))
        conn.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS first_name VARCHAR;"))
        conn.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS last_name VARCHAR;"))
        conn.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;"))

        conn.execute(text("ALTER TABLE api_keys ADD COLUMN IF NOT EXISTS password VARCHAR;"))
        conn.execute(text("ALTER TABLE api_keys ADD COLUMN IF NOT EXISTS is_active BOOLEAN DEFAULT TRUE;"))
        conn.execute(text("ALTER TABLE api_keys ADD COLUMN IF NOT EXISTS last_used_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;"))


__all__ = ["init_db", "get_connection", "session", "engine", "get_db"]
