from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict
from acb_orm.schemas.log_schema import LogCreate, LogRead, LogUpdate
from acb_orm.enums.status_visual_resource import StatusVisualResource
from acb_orm.enums.file_type import FileType
from acb_orm.schemas.access_config_schema import AccessConfigCreate, AccessConfigUpdate, AccessConfigRead


class VisualResourcesBase(BaseModel):
    """
    Base schema for the visual resources document.
    Contains common fields for creation and reading.
    """
    file_url: str = Field(..., description="URL or path to the file.")
    file_name: str = Field(..., description="Original name of the file.")
    file_type: FileType = Field(..., description="Type of the file.")
    status: StatusVisualResource = Field(..., description="Status of the visual resource.")

class VisualResourcesCreate(VisualResourcesBase):
    """
    Creation schema for the visual resources document.
    All fields are required when creating a new document.
    """
    log: Optional[LogCreate] = Field(None, description="Audit log.")
    access_config: AccessConfigCreate = Field(..., description="Access configuration.")

class VisualResourcesUpdate(BaseModel):
    """
    Update schema for the visual resources document.
    Only contains fields that are modified during an update.
    The log will be handled by the service layer.
    """
    file_name: Optional[str] = Field(None, description="Original name of the file.")
    file_type: Optional[FileType] = Field(None, description="Type of the file.")
    status: Optional[StatusVisualResource] = Field(None, description="Status of the visual resource.")
    access_config: Optional[AccessConfigUpdate] = Field(None, description="Access configuration.")
    log: Optional[LogUpdate] = Field(None, description="Audit log.")

class VisualResourcesRead(VisualResourcesBase):
    """
    Read schema for the visual resources document.
    Complete representation including the document ID.
    """
    id: str = Field(..., description="ObjectId of the visual resource.")
    access_config: AccessConfigRead = Field(..., description="Access configuration.")
    log: LogRead = Field(..., description="Audit log.")

    model_config = ConfigDict(from_attributes=True)