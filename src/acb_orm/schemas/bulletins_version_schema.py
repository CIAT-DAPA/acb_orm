from typing import Optional, Any, Dict
from pydantic import BaseModel, Field, ConfigDict, field_validator
from acb_orm.schemas.log_schema import LogCreate, LogUpdate, LogRead
from acb_orm.collections.bulletins_master import BulletinsMaster
from acb_orm.collections.bulletins_version import BulletinsVersion
from acb_orm.validations.valid_reference_id import validate_reference_id

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
    bulletin_master_id: str = Field(..., description="ObjectId of the bulletin master document.")
    previous_version_id: Optional[str] = Field(None, description="ObjectId of the previous bulletin version.")
    log: Optional[LogCreate] = Field(None, description="Audit log.")

    @field_validator('bulletin_master_id')
    def validate_bulletin_master_id(cls, v):
        return validate_reference_id(v, BulletinsMaster)

    @field_validator('previous_version_id')
    def validate_previous_version_id(cls, v):
        if v is not None:
            return validate_reference_id(v, BulletinsVersion)
        return v

class BulletinsVersionUpdate(BaseModel):
    """
    Update schema for the bulletin version document.
    Since versions are immutable, this schema is intended for very specific
    updates, and the log is handled by the service layer.
    """
    bulletin_master_id: Optional[str] = Field(..., description="ObjectId of the bulletin master document.")
    previous_version_id: Optional[str] = Field(None, description="ObjectId of the previous bulletin version.")
    log: Optional[LogUpdate] = Field(None, description="Audit log.")
    data: Optional[Dict[str, Any]] = Field(None, description="Updated user-specific data.")

    @field_validator('bulletin_master_id')
    def validate_bulletin_master_id(cls, v):
        if v is not None:
            return validate_reference_id(v, BulletinsMaster)
        return v

    @field_validator('previous_version_id')
    def validate_previous_version_id(cls, v):
        if v is not None:
            return validate_reference_id(v, BulletinsVersion)
        return v

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