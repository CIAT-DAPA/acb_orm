from enum import Enum

class ExportFormat(str, Enum):
    PDF = "pdf"
    JPG = "jpg"
    JSON = "json"
    HTML = "html"
