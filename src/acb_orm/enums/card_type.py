from enum import Enum

class CardType(Enum):
    PEST_OR_DISEASE = "pest_or_disease"
    CROP_INFO = "crop_info"
    RECOMMENDATION = "recommendation"
    WEATHER_ALERT = "weather_alert"
    GENERAL = "general"