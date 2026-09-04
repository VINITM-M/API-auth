
from default_settings import schema_settings

class APIKeyAuthConfig:

    @property
    def api_key_schema_class(self):

        return self.get_optional_paths(
            f"{self.prefix}API_APIKEY_SCHEMA_CLASS",
            schema_settings.apikey_schema_class,
        )