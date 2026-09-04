
from dataclasses import dataclass, field

@dataclass(frozen=True)
class DefaultSchemaSettings():

    user_schema_class: Optional[str] = None
    apikey_schema_class: Optional[str] = None
    user_schema_fields: List[str] = field(
        default_factory=lambda: ["id", "username", "email"]
    )


schema_settings = DefaultSchemaSettings()