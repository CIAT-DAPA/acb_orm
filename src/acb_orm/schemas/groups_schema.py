from typing import Optional, List, Dict
from pydantic import BaseModel, Field, ConfigDict
from acb_orm.schemas.log_schema import LogCreate, LogRead, LogUpdate
from acb_orm.schemas.user_access_schema import UserAccessCreate, UserAccessUpdate, UserAccessRead

class GroupsBase(BaseModel):
    """
    Base schema for the groups document.
    Contains common fields for creation and reading.
    """
    group_name: str = Field(..., description="Name of the group.")
    country: str = Field(..., description="Country code (e.g., 'CO').")
    description: Optional[str] = Field(None, description="Description of the group.")

class GroupsCreate(GroupsBase):
    """
    Creation schema for the groups document.
    All fields are required when creating a new document.
    """
    users_access: List[UserAccessCreate] = Field(..., description="List of users and their roles within the group.")
    log: Optional[LogCreate] = Field(None, description="Audit log.")
    
class GroupsUpdate(BaseModel):
    """
    Update schema for the groups document.
    The log and users_access fields will be handled by the service layer.
    """
    group_name: Optional[str] = Field(None, description="Name of the group.")
    country: Optional[str] = Field(None, description="Country code (e.g., 'CO').")
    description: Optional[str] = Field(None, description="Description of the group.")
    log: Optional[LogUpdate] = Field(None, description="Audit log.")
    users_access: Optional[List[UserAccessUpdate]] = Field(None, description="List of users and their roles within the group.")

class GroupsRead(GroupsBase):
    """
    Read schema for the groups document.
    Complete representation including the document ID.
    """
    id: str = Field(..., description="ObjectId of the group.")
    users_access: List[UserAccessRead] = Field(..., description="List of users and their roles within the group.")
    log: LogRead = Field(..., description="Audit log.")
    model_config = ConfigDict(from_attributes=True)
