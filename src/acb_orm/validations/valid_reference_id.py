from bson import ObjectId
from mongoengine import Document, DoesNotExist

def validate_reference_id(value: str, document_cls: type) -> str:
    """
    Validates that the value is a valid ObjectId and that the referenced document exists.
    """
    if not ObjectId.is_valid(value):
        raise ValueError(f"Invalid ObjectId format for ID: '{value}'")
    if document_cls:
        try:
            document_cls.objects.get(id=value)
        except DoesNotExist:
            raise ValueError(f"Referenced document with ID '{value}' does not exist.")
    return value
