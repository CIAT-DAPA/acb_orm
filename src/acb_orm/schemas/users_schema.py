from typing import Optional
from pydantic import BaseModel, Field, ConfigDict
from acb_orm.schemas.log_schema import LogCreate, LogRead, LogUpdate

class UsersBase(BaseModel):
    """
    Base schema for the users document.
    Contains common fields for creation and reading.
    """
    ext_id: str = Field(..., description="External unique ID of the user.")
    is_active: Optional[bool] = Field(True, description="Indicates if the user account is active.")

class UsersCreate(UsersBase):
    """
    Creation schema for the users document.
    All fields are required when creating a new document.
    """
    log: Optional[LogCreate] = Field(..., description="Audit log.")
    
class UsersUpdate(BaseModel):
    """
    Update schema for the users document.
    The log will be handled by the service layer.
    """
    is_active: Optional[bool] = Field(None, description="Indicates if the user account is active.")
    log: Optional[LogUpdate] = Field(None, description="Audit log.")

class UsersRead(UsersBase):
    """
    Read schema for the users document.
    Complete representation including the document ID.
    """
    id: str = Field(..., description="ObjectId of the user.")
    log: Optional[LogRead] = Field(..., description="Audit log.")
    model_config = ConfigDict(from_attributes=True)
