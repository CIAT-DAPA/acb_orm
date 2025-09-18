from typing import Optional, Any, Dict
from pydantic import BaseModel, Field, ConfigDict
from acb_orm.schemas.log_schema import LogCreate, LogUpdate, LogRead
from acb_orm.collections.bulletins_master import BulletinsMaster
from acb_orm.collections.bulletins_version import BulletinsVersion
from acb_orm.validations.valid_reference_id import ValidReferenceId

class BulletinsVersionBase(BaseModel):
    """
    Base schema for the bulletin version document.
    Contains common fields for creation and reading.
    """
    version_num: str = Field(..., description="Version number of the bulletin.")
    data: Dict[str, Any] = Field(..., description="User-specific data for the bulletin content.")

class BulletinsVersionCreate(BulletinsVersionBase):
    """
    Creation schema for the bulletin version document.
    All fields are required when creating a new document.
    """
    bulletin_master_id: ValidReferenceId[BulletinsMaster] = Field(..., description="ObjectId of the bulletin master document.")
    previous_version_id: Optional[ValidReferenceId[BulletinsVersion]] = Field(None, description="ObjectId of the previous bulletin version.")
    log: LogCreate = Field(..., description="Audit log.")
    
class BulletinsVersionUpdate(BaseModel):
    """
    Update schema for the bulletin version document.
    Since versions are immutable, this schema is intended for very specific
    updates, and the log is handled by the service layer.
    """
    bulletin_master_id: Optional[ValidReferenceId[BulletinsMaster]] = Field(..., description="ObjectId of the bulletin master document.")
    previous_version_id: Optional[ValidReferenceId[BulletinsVersion]] = Field(None, description="ObjectId of the previous bulletin version.")
    log: Optional[LogUpdate] = Field(..., description="Audit log.")
    data: Optional[Dict[str, Any]] = Field(None, description="Updated user-specific data.")

class BulletinsVersionRead(BulletinsVersionBase):
    """
    Read schema for the bulletin version document.
    Complete representation including the document ID.
    """
    id: str = Field(..., description="ObjectId of the bulletin version document.")
    bulletin_master_id: str = Field(..., description="ObjectId of the bulletin master document.")
    previous_version_id: Optional[str] = Field(None, description="ObjectId of the previous bulletin version.")
    log: LogRead = Field(..., description="Audit log.")
    model_config = ConfigDict(from_attributes=True)