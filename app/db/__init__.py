"""Database package initialization."""

from db.db import get_connection, SessionLocal


def init_db():
    """Create application tables at startup using ORM metadata."""
    from models.api_key import Base
    from db.db import engine

    Base.metadata.create_all(engine)


__all__ = ["init_db", "get_connection", "SessionLocal"]
