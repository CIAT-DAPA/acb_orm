from typing import Optional
from pydantic import BaseModel, Field, field_validator
from acb_orm.validations.valid_reference_id import validate_reference_id
from acb_orm.collections.users import User
from acb_orm.collections.roles import Role

class UserAccessCreate(BaseModel):
    """
    Creation schema for a new UserAccess document.
    """
    user_id: str = Field(..., description="The unique ID of the user.")
    role_id: str = Field(..., description="The unique ID of the role assigned to the user.")

    @field_validator('user_id')
    def validate_user_id(cls, v):
        return validate_reference_id(v, User)

    @field_validator('role_id')
    def validate_role_id(cls, v):
        return validate_reference_id(v, Role)

class UserAccessUpdate(BaseModel):
    """
    Update schema for an existing UserAccess document.
    """
    user_id: Optional[str] = Field(None, description="The unique ID of the user.")
    role_id: Optional[str] = Field(None, description="The unique ID of the role assigned to the user.")

    @field_validator('user_id')
    def validate_user_id(cls, v):
        if v is not None:
            return validate_reference_id(v, User)
        return v

    @field_validator('role_id')
    def validate_role_id(cls, v):
        if v is not None:
            return validate_reference_id(v, Role)
        return v

class UserAccessRead(BaseModel):
    """
    Read schema for a UserAccess document.
    """
    user_id: str = Field(..., description="The unique ID of the user.")
    role_id: str = Field(..., description="The unique ID of the role assigned to the user.")
