from typing import Optional, Any, Dict, List
from pydantic import BaseModel, Field, ConfigDict
from acb_orm.schemas.log_schema import LogCreate, LogRead, LogUpdate

class RolesBase(BaseModel):
    """
    Base schema for the roles document.
    Contains common fields for creation and reading.
    """
    role_name: str = Field(..., description="Name of the role.")
    description: Optional[str] = Field(None, description="Description of the role.")
    permissions: Dict[str, Any] = Field({}, description="Dictionary of permissions associated with the role.")

class RolesCreate(RolesBase):
    """
    Creation schema for the roles document.
    All fields are required when creating a new document.
    """
    log: Optional[LogCreate] = Field(None, description="Audit log.")
    
class RolesUpdate(BaseModel):
    """
    Update schema for the roles document.
    The log will be handled by the service layer.
    """
    role_name: Optional[str] = Field(None, description="Name of the role.")
    description: Optional[str] = Field(None, description="Description of the role.")
    permissions: Optional[Dict[str, Any]] = Field(None, description="Dictionary of permissions associated with the role.")
    log: Optional[LogUpdate] = Field(None, description="Audit log.")

class RolesRead(RolesBase):
    """
    Read schema for the roles document.
    Complete representation including the document ID.
    """
    id: str = Field(..., description="ObjectId of the role.")
    log: LogRead = Field(..., description="Audit log.")
    model_config = ConfigDict(from_attributes=True)
