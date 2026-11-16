from urllib.parse import quote_plus
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from core import config


def get_connection():
    encoded_password = quote_plus(config.password or "")
    engine = create_engine(
        f"postgresql+psycopg2://{config.user}:{encoded_password}@{config.host}:{config.port}/{config.database}",
        pool_pre_ping=True,
        pool_size=10,
        max_overflow=20
    )
    return engine


engine = get_connection()

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Scoped session for thread-safety and cleanup
ScopedSession = scoped_session(SessionLocal)
session = ScopedSession


@contextmanager
def get_db():
    """Context manager for database sessions with automatic rollback and cleanup."""
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
