from enum import Enum

class IntegrationServiceType(Enum):
    WEATHER = "weather"
    DISTRIBUTION = "distribution"
    RECOMMENDATIONS = "recommendations"
    GEOCODING = "geocoding"
    OTHER = "other"
