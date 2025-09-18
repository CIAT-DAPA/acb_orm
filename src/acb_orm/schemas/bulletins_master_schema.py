from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict
from acb_orm.schemas.log_schema import LogCreate, LogUpdate, LogRead
from acb_orm.enums.status_bulletin import StatusBulletin
from acb_orm.schemas.access_config_schema import AccessConfigCreate, AccessConfigUpdate, AccessConfigRead
from acb_orm.collections.templates_master import TemplatesMaster
from acb_orm.collections.templates_version import TemplatesVersion
from acb_orm.collections.bulletins_version import BulletinsVersion
from acb_orm.validations.valid_reference_id import ValidReferenceId

class BulletinsMasterBase(BaseModel):
    """
    Base schema for the bulletin master document.
    Contains common fields for reading and creation.
    """
    bulletin_name: str = Field(..., description="Name of the bulletin.")
    status: Optional[StatusBulletin] = Field(StatusBulletin.DRAFT, description="Current status of the bulletin.")

class BulletinsMasterCreate(BulletinsMasterBase):
    """
    Creation schema for the bulletin master document.
    All fields are required when creating a new document.
    """
    base_template_master_id: ValidReferenceId[TemplatesMaster] = Field(..., description="ObjectId of the base template master.")
    base_template_version_id: ValidReferenceId[TemplatesVersion] = Field(..., description="ObjectId of the specific base template version.")
    current_version_id: Optional[ValidReferenceId[BulletinsVersion]] = Field(None, description="ObjectId of the current bulletin version.")
    access_config: AccessConfigCreate = Field(..., description="Access configuration.")
    log: LogCreate = Field(..., description="Audit log.")
    
class BulletinsMasterUpdate(BaseModel):
    """
    Update schema for the bulletin master document.
    Only contains fields that are modified during an update.
    All fields are optional to allow for partial updates.
    """
    bulletin_name: Optional[str] = Field(None, description="Name of the bulletin.")
    status: Optional[StatusBulletin] = Field(None, description="Current status of the bulletin.")
    base_template_master_id: Optional[ValidReferenceId[TemplatesMaster]] = Field(None, description="ObjectId of the base template master.")
    base_template_version_id: Optional[ValidReferenceId[TemplatesVersion]] = Field(None, description="ObjectId of the specific base template version.")
    current_version_id: Optional[ValidReferenceId[BulletinsVersion]] = Field(None, description="ObjectId of the current bulletin version.")
    access_config: Optional[AccessConfigUpdate] = Field(None, description="Access configuration.")
    log: LogUpdate = Field(..., description="Audit log.")

class BulletinsMasterRead(BulletinsMasterBase):
    """
    Read schema for the bulletin master document.
    Complete representation including the document ID.
    """
    id: str = Field(..., description="ObjectId of the bulletin master.")
    base_template_master_id: str = Field(..., description="ObjectId of the base template master.")
    base_template_version_id: str = Field(..., description="ObjectId of the specific base template version.")
    current_version_id: Optional[str] = Field(None, description="ObjectId of the current bulletin version.")
    access_config: AccessConfigRead = Field(..., description="Access configuration.")
    log: LogRead = Field(..., description="Audit log.")
    model_config = ConfigDict(from_attributes=True)