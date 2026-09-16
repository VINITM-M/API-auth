
from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel, ConfigDict, Field

# Re-export table utilities if imported from schemas
from db.table_insertion import api_info_table_insert, apikey


class APIKeyRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(description="Unique identifier of the API key.")
    user: Optional[Dict[str, Any]] = Field(
        default=None, description="The user associated with this API key."
    )
    key: str = Field(description="The API key string, generated on creation.")
    created_at: datetime = Field(
        description="The date and time when the API key was created."
    )
    expires_at: Optional[datetime] = Field(
        default=None, description="The date and time when the API key will expire."
    )
    is_active: bool = Field(
        description="Indicates whether the API key is currently active and usable."
    )
    requests_count: int = Field(
        description="Number of requests made with this API key."
    )
    max_requests: Optional[int] = Field(
        default=None,
        description="Maximum number of requests allowed (total or per reset period).",
    )
    reset_at: Optional[datetime] = Field(
        default=None, description="Time when the request count resets, if applicable."
    )


class APIKeyCreate(BaseModel):
    """The payload accepted when creating an API key.

    The key itself, the request counter, the quota and the reset time are all
    server generated, so only ownership, expiration and the active flag can be
    supplied.
    """

    user_id: Optional[int] = Field(
        default=None,
        description="The ID of the user associated with this APIKey (Optional).",
    )
    expires_at: Optional[datetime] = Field(
        default=None,
        description="The date and time when the API key will expire. Leave blank for no expiration.",
    )
    is_active: bool = Field(
        default=True,
        description="Indicates whether the API key is currently active and usable.",
    ) 