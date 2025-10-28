from enum import Enum

class AuthType(Enum):
    NONE = "none"
    API_KEY = "api_key"
    BASIC = "basic"
    OAUTH2 = "oauth2"
    BEARER = "bearer"
