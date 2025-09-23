from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict, field_validator
from acb_orm.schemas.log_schema import LogCreate, LogUpdate, LogRead
from acb_orm.enums.status_template import StatusTemplate
from acb_orm.schemas.access_config_schema import AccessConfigCreate, AccessConfigUpdate, AccessConfigRead
from acb_orm.validations.valid_reference_id import validate_reference_id
from acb_orm.collections.templates_version import TemplatesVersion

class TemplatesMasterBase(BaseModel):
    """
    Base schema for the template master document.
    Contains common fields for reading and creation.
    """
    template_name: str = Field(..., description="Template name.")
    description: Optional[str] = Field(None, description="Template description.")
    status: StatusTemplate = Field(..., description="Current status of the template.")

class TemplatesMasterCreate(TemplatesMasterBase):
    """
    Creation schema for the template master document.
    All fields are required when creating a new document.
    """
    current_version_id: Optional[str] = Field(None, description="ObjectId of the current version.")
    access_config: AccessConfigCreate = Field(..., description="Access configuration.")
    log: Optional[LogCreate] = Field(None, description="Audit log.")

    @field_validator('current_version_id')
    def validate_current_version_id(cls, v):
        if v is not None:
            return validate_reference_id(v, TemplatesVersion)
        return v

class TemplatesMasterUpdate(BaseModel):
    """
    Update schema for the template master document.
    Only contains fields that are modified during an update.
    All fields are optional to allow for partial updates.
    """
    template_name: Optional[str] = Field(None, description="Template name.")
    description: Optional[str] = Field(None, description="Template description.")
    status: Optional[StatusTemplate] = Field(None, description="Current status of the template.")
    current_version_id: Optional[str] = Field(None, description="ObjectId of the current version.")
    access_config: Optional[AccessConfigUpdate] = Field(None, description="Access configuration.")
    log: Optional[LogUpdate] = Field(None, description="Audit log.")

    @field_validator('current_version_id')
    def validate_current_version_id(cls, v):
        if v is not None:
            return validate_reference_id(v, TemplatesVersion)
        return v

class TemplatesMasterRead(TemplatesMasterBase):
    """
    Read schema for the template master document.
    Complete representation including the document ID.
    """
    id: str = Field(..., description="ObjectId of the template master.")
    access_config: AccessConfigRead = Field(..., description="Access configuration.")
    current_version_id: Optional[str] = Field(None, description="ObjectId of the current version.")
    log: LogRead = Field(..., description="Audit log.")
    model_config = ConfigDict(from_attributes=True)
