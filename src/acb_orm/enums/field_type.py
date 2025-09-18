from enum import Enum

class FieldType(Enum):
    TEXT = "text"
    CLIMATE_DATA_PUNTUAL = "climate_data_puntual"
    LIST = "list"
    SELECT = "select"
    SELECT_WITH_ICONS = "select_with_icons"
    SELECT_BACKGROUND = "select_background"
    NUMBER = "number"
    DATE = "date"
    DATE_RANGE = "date_range"
    IMAGE_UPLOAD = "image_upload"
    ALGORITHM = "algorithm"
    PAGE_NUMBER = "page_number"
    CARD = "card"