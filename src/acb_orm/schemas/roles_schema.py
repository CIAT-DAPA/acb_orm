from typing import Optional, Any, Dict, List
from pydantic import BaseModel, Field, ConfigDict
from acb_orm.schemas.log_schema import LogCreate, LogRead, LogUpdate

class RolePermissionSchema(BaseModel):
    """
    Schema for CRUD permissions of a module.
    """
    c: bool = Field(False, description="Create permission")
    r: bool = Field(False, description="Read permission")
    u: bool = Field(False, description="Update permission")
    d: bool = Field(False, description="Delete permission")

class RolesBase(BaseModel):
    """
    Base schema for the roles document.
    Contains common fields for creation and reading.
    """
    role_name: str = Field(..., description="Name of the role.")
    description: Optional[str] = Field(None, description="Description of the role.")
    permissions: Dict[str, RolePermissionSchema] = Field(
        ...,
        description="Dictionary of permissions per module. Each key is a module name, value is CRUD permissions."
    )

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
    permissions: Optional[Dict[str, RolePermissionSchema]] = Field(
        None,
        description="Dictionary of permissions per module. Each key is a module name, value is CRUD permissions."
    )
    log: Optional[LogUpdate] = Field(None, description="Audit log.")

class RolesRead(RolesBase):
    """
    Read schema for the roles document.
    Complete representation including the document ID.
    """
    id: str = Field(..., description="ObjectId of the role.")
    log: LogRead = Field(..., description="Audit log.")
    model_config = ConfigDict(from_attributes=True)
