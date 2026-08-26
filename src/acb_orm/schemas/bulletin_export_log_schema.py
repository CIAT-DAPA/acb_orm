from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict, field_validator
from acb_orm.enums.export_format import ExportFormat
from acb_orm.collections.users import User
from acb_orm.collections.bulletins_master import BulletinsMaster
from acb_orm.collections.bulletins_version import BulletinsVersion
from acb_orm.validations.valid_reference_id import validate_reference_id

class BulletinExportLogBase(BaseModel):
    """
    Base schema for the bulletin export log document.
    Contains common fields for creation and reading.
    """
    format: ExportFormat = Field(..., description="Format in which the bulletin was exported.")
    bulletin_title: Optional[str] = Field(None, description="Title of the bulletin at the moment of the export.")

class BulletinExportLogCreate(BulletinExportLogBase):
    """
    Creation schema for the bulletin export log document.
    All fields are required when registering a new export action.
    """
    user_id: str = Field(..., description="ObjectId of the user who performed the export.")
    bulletin_master_id: str = Field(..., description="ObjectId of the bulletin master document.")
    bulletin_version_id: str = Field(..., description="ObjectId of the exported bulletin version.")
    exported_at: Optional[datetime] = Field(default_factory=datetime.now, description="The date and time the export was performed.")

    @field_validator('user_id')
    def validate_user_id(cls, v):
        return validate_reference_id(v, User)

    @field_validator('bulletin_master_id')
    def validate_bulletin_master_id(cls, v):
        return validate_reference_id(v, BulletinsMaster)

    @field_validator('bulletin_version_id')
    def validate_bulletin_version_id(cls, v):
        return validate_reference_id(v, BulletinsVersion)

class BulletinExportLogUpdate(BaseModel):
    """
    Update schema for the bulletin export log document.
    Export logs are append-only records, so only descriptive fields
    can be corrected by the service layer.
    """
    format: Optional[ExportFormat] = Field(None, description="Format in which the bulletin was exported.")
    bulletin_title: Optional[str] = Field(None, description="Title of the bulletin at the moment of the export.")

class BulletinExportLogRead(BulletinExportLogBase):
    """
    Read schema for the bulletin export log document.
    Complete representation including the document ID.
    """
    id: str = Field(..., description="ObjectId of the bulletin export log document.")
    user_id: str = Field(..., description="ObjectId of the user who performed the export.")
    user_first_name: Optional[str] = Field(None, description="First name of the user who performed the export.")
    user_last_name: Optional[str] = Field(None, description="Last name of the user who performed the export.")
    bulletin_master_id: str = Field(..., description="ObjectId of the bulletin master document.")
    bulletin_version_id: str = Field(..., description="ObjectId of the exported bulletin version.")
    exported_at: datetime = Field(..., description="The date and time the export was performed.")
    model_config = ConfigDict(from_attributes=True)
