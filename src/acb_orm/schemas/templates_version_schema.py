from typing import Optional, Dict, Any
from pydantic import BaseModel, Field, ConfigDict, field_validator
from acb_orm.schemas.log_schema import LogCreate, LogUpdate, LogRead
from acb_orm.validations.valid_reference_id import validate_reference_id
from acb_orm.collections.templates_master import TemplatesMaster
from acb_orm.collections.templates_version import TemplatesVersion

class TemplatesVersionBase(BaseModel):
    """
    Base schema for the template version document.
    Contains common fields for reading and creation.
    """
    version_num: str = Field(..., description="Version number or identifier.")
    commit_message: str = Field(..., description="Message describing the changes in this version.")
    content: Dict[str, Any] = Field(..., description="Complete structure and design of the template version.")

class TemplatesVersionCreate(TemplatesVersionBase):
    """
    Creation schema for the template version document.
    All fields are required when creating a new document.
    """
    template_master_id: str = Field(..., description="ObjectId of the associated template master.")
    previous_version_id: Optional[str] = Field(None, description="ObjectId of the previous version.")
    log: LogCreate = Field(..., description="Audit log.")

    @field_validator('template_master_id')
    def validate_template_master_id(cls, v):
        return validate_reference_id(v, TemplatesMaster)

    @field_validator('previous_version_id')
    def validate_previous_version_id(cls, v):
        if v is not None:
            return validate_reference_id(v, TemplatesVersion)
        return v

class TemplatesVersionUpdate(BaseModel):
    """
    Update schema for the template version document.
    Only contains fields that are modified during an update.
    All fields are optional to allow for partial updates.
    """
    version_num: Optional[str] = Field(None, description="Version number or identifier.")
    previous_version_id: Optional[str] = Field(None, description="ObjectId of the previous version.")
    log: Optional[LogUpdate] = Field(None, description="Audit log.")
    commit_message: Optional[str] = Field(None, description="Message describing the changes in this version.")
    content: Optional[Dict[str, Any]] = Field(None, description="Complete structure and design of the template version.")

    @field_validator('previous_version_id')
    def validate_previous_version_id(cls, v):
        if v is not None:
            return validate_reference_id(v, TemplatesVersion)
        return v

class TemplatesVersionRead(TemplatesVersionBase):
    """
    Read schema for the template version document.
    Complete representation including the document ID.
    """
    id: str = Field(..., description="ObjectId of the template version.")
    template_master_id: str = Field(..., description="ObjectId of the associated template master.")
    previous_version_id: Optional[str] = Field(None, description="ObjectId of the previous version.")
    log: LogRead = Field(..., description="Audit log.")
    model_config = ConfigDict(from_attributes=True)
