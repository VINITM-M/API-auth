"""Database package initialization."""


from db.db import get_connection


def init_db():
    """Create application tables at startup without circular imports."""
    from db.table_insertion import table_creation

    table_creation()


__all__ = ["init_db", "get_connection"]
