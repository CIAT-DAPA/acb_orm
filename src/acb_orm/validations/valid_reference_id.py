from typing import Type, Any
from pydantic import GetCoreSchemaHandler
from pydantic_core import CoreSchema, core_schema
from mongoengine import Document, DoesNotExist
from bson import ObjectId

class ValidReferenceId(str):
    """
    Custom Pydantic type to validate a MongoDB ObjectId string and ensure
    that the referenced document exists in the specified collection.
    
    Usage:
    - field_name: ValidReferenceId = Field(...)
    - field_name: ValidReferenceId[User] = Field(...) # With a specific MongoEngine Document class
    """

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source: Type[Any], handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        """
        Creates a custom Pydantic CoreSchema for this type.
        """
        # Get the MongoEngine Document class from the type annotation
        ref_document_cls = getattr(cls, '__mongoengine_document__', None)

        def validate_reference(value: str, other: Any) -> str:
            """
            Validates if the value is a valid ObjectId and if the document exists.
            """
            # Check for a valid ObjectId format
            if not ObjectId.is_valid(value):
                raise ValueError(f"Invalid ObjectId format for ID: '{value}'")

            #print(other)

            # If a reference document class is provided, check for existence
            if ref_document_cls:
                try:
                    ref_document_cls.objects.get(id=value)
                except DoesNotExist:
                    raise ValueError(f"Referenced document with ID '{value}' does not exist.")
            
            return value

        # The schema uses a string type with a function to validate it.
        return core_schema.with_info_plain_validator_function(validate_reference)

    @classmethod
    def __class_getitem__(cls, item: Type[Document]) -> Type:
        """
        Allows us to use ValidReferenceId[User] to specify the document class.
        """
        new_cls = type(
            f"{cls.__name__}[{item.__name__}]",
            (cls,),
            {
                '__mongoengine_document__': item,
            },
        )
        return new_cls
