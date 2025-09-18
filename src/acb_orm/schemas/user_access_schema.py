from typing import Optional
from pydantic import BaseModel, Field

from acb_orm.validations.valid_reference_id import ValidReferenceId
from acb_orm.collections.users import User
from acb_orm.collections.roles import Role

class UserAccessCreate(BaseModel):
    """
    Creation schema for a new UserAccess document.
    """
    user_id: ValidReferenceId[User] = Field(..., description="The unique ID of the user.")
    role_id: ValidReferenceId[Role] = Field(..., description="The unique ID of the role assigned to the user.")

class UserAccessUpdate(BaseModel):
    """
    Update schema for an existing UserAccess document.
    """
    user_id: Optional[ValidReferenceId[User]] = Field(None, description="The unique ID of the user.")
    role_id: Optional[ValidReferenceId[Role]] = Field(None, description="The unique ID of the role assigned to the user.")

class UserAccessRead(BaseModel):
    """
    Read schema for a UserAccess document.
    """
    user_id: str = Field(..., description="The unique ID of the user.")
    role_id: str = Field(..., description="The unique ID of the role assigned to the user.")
