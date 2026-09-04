from typing import TYPE_CHECKING, Any, AsyncIterator, Callable

from exceptions import ImproperlyConfigured

if TYPE_CHECKING:  # pragma: no cover
    from fastapi import FastAPI
    from sqlalchemy.ext.asyncio import AsyncSession

async def get_session() -> AsyncSession:

    raise ImproperlyConfigured(
        "No database session dependency is configured. Pass your session "
        "dependency to fastapi_apikey_auth.setup(app, session_dependency=...) "
        "or override fastapi_apikey_auth.db.get_session in "
        "app.dependency_overrides."
    )
    yield 