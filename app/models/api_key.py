from unittest.mock import Base
from app.core import config
from sqlalchemy.orm import Mapped, Integer, mapped_column 
from sqlalchemy import Column, Integer, String, DateTime, func 
import app.utils.timezone import now  
from fastapi import Depends, Optional
from datetime import datetime, timedelta
import secrets 

#: Number of random bytes used to build a key. ``secrets.token_urlsafe(48)``
#: produces a 64 character URL-safe string, which is what ``key`` stores.
KEY_ENTROPY_BYTES = 48


def default_max_requests() -> Optional[int]:
    """Return the configured request quota applied to freshly created keys.

    Returns:
        Optional[int]: The value of ``APIKEY_AUTH_MAX_REQUESTS``, or ``None``
        when no quota is configured.

    """
    return config.max_requests

def generate_key():
    """Generate a new, cryptographically secure API key.

    Returns:
        str: A 64 character URL-safe key.

    """
    return secrets.token_urlsafe(KEY_ENTROPY_BYTES)


class APIKey(Base):

    __tablename__ = "apikey_auth_api_key"

    id : Mapped[int] = mapped_column(
        Integer, 
        primary_key=True, 
        autoincrement=True
    )

    user_id : Mapped[int] = mapped_column(
        Integer,
        nullable=True,
        index=True,
        doc="The user associated with this API key.",
    )

    #generating key
    key: Mapped[str] = mapped_column(
        String(64),
        unique=True,
        index=True,
        default=generate_key,
        doc="The API key used for authentication.",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=now,
        doc="Timestamp when the API key was generated.",
    )

    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        doc="Timestamp when the API key will expire.",
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        doc="Status flag to enable or disable the API key.",
    )
    requests_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
        doc="Tracks the total number of requests made using this API key.",
    )
    max_requests: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
        default=default_max_requests,
        doc="Defines the maximum allowed requests, either total or per reset interval.",
    )
    reset_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        default=lambda: APIKey.calculate_next_reset(),
        doc="Timestamp when the request count will reset, if rate limiting is time-based.",
    )

    @staticmethod 
    def calculate_next_reset() -> Optional[datetime]:

        """Calculate the next reset time based on the configured reset
        interval.

        Uses the reset_requests_interval from config to determine the interval
        (minutely, hourly, daily, monthly, or None). Returns None if no interval is set.

        Returns:
            Optional[datetime]: The next reset time or None if no reset interval is configured.

        """

        interval = config.reset_requests_interval

        if not interval:
            return None 

        if interval == "minutely":
            return now() + datetime.timedelta(minutes=1) 

        elif interval == "hourly":
            return now() + datetime.timedelta(hours=1) 

        elif interval == "daily": 
            return now() + datetime.timedelta(days=1) 

        elif interval == "monthly":
            return now() + datetime.timedelta(days=30) 

        return now() + datetime.timedelta(days=30)  # Default to monthly if unrecognized 