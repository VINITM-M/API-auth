"""Database package initialization."""

from database.db import get_connection, session


def init_db():
    """Create application tables at startup using ORM metadata."""
    from Schemas.api_key import Base
    from database.db import engine

    Base.metadata.create_all(engine)


__all__ = ["init_db", "get_connection", "session"]
