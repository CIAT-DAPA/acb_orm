from typing import Optional, List
from pydantic import BaseModel, Field, model_validator
from acb_orm.enums.access_type import AccessType
from acb_orm.validations.valid_reference_id import ValidReferenceId
from acb_orm.collections.groups import Group

class AccessConfigCreate(BaseModel):
    """
    Creation schema for access configuration.
    It inherits the base validation logic.
    """
    access_type: AccessType = Field(..., description="The type of access to the document.")
    allowed_groups: List[ValidReferenceId[Group]] = Field([], description="List of allowed group IDs.")
    
    @model_validator(mode='after')
    def validate_groups_for_access_type(self):
        """
        Ensures that 'allowed_groups' is empty for public access and not empty
        for restricted or private access.
        """
        if self.access_type == AccessType.PUBLIC:
            self.allowed_groups = []
        elif not self.allowed_groups:
            raise ValueError("allowed_groups must not be empty for non-public access.")
        return self

class AccessConfigUpdate(BaseModel):
    """
    Update schema for access configuration.
    All fields are optional to allow for partial updates.
    """
    access_type: Optional[AccessType] = Field(None, description="The type of access to the document.")
    allowed_groups: Optional[List[ValidReferenceId[Group]]] = Field(None, description="List of allowed group IDs.")

    @model_validator(mode='after')
    def validate_groups_on_update(self):
        """
        Validates allowed_groups based on the provided access_type.
        """
        if self.access_type == AccessType.PUBLIC:
            self.allowed_groups = []
        elif self.access_type is not None and not self.allowed_groups:
            raise ValueError("allowed_groups must not be empty for non-public access.")
        return self

class AccessConfigRead(BaseModel):
    """
    Read schema for access configuration.
    It is a standalone schema to avoid re-validating the IDs.
    """
    access_type: AccessType = Field(..., description="The type of access to the document.")
    allowed_groups: Optional[List[str]] = Field(None, description="List of allowed group IDs.")