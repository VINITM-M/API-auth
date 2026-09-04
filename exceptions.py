class APIKeyAuthError(Exception):
    """Base class for every error raised by ``fastapi-apikey-auth``."""


class ImproperlyConfigured(APIKeyAuthError):
    """Raised when the package is used with an invalid configuration.

    This mirrors the behaviour of Django's system check framework: the
    configuration is validated up-front so that misconfigured projects fail
    loudly at startup instead of misbehaving at request time.

    """