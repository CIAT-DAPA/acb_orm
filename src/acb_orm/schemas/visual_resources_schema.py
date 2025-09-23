from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict
from acb_orm.schemas.log_schema import LogCreate, LogRead, LogUpdate


class VisualResourcesBase(BaseModel):
    """
    Base schema for the visual resources document.
    Contains common fields for creation and reading.
    """
    file_url: str = Field(..., description="URL or path to the file.")
    file_name: str = Field(..., description="Original name of the file.")
    file_type: str = Field(..., description="MIME type of the file (e.g., 'image/jpeg').")
    tags: Optional[List[str]] = Field(None, description="Tags for search and organization.")


class VisualResourcesCreate(VisualResourcesBase):
    """
    Creation schema for the visual resources document.
    All fields are required when creating a new document.
    """
    log: Optional[LogCreate] = Field(..., description="Audit log.")


class VisualResourcesUpdate(BaseModel):
    """
    Update schema for the visual resources document.
    Only contains fields that are modified during an update.
    The log will be handled by the service layer.
    """
    file_name: Optional[str] = Field(None, description="Original name of the file.")
    file_type: Optional[str] = Field(None, description="MIME type of the file (e.g., 'image/jpeg').")
    tags: Optional[List[str]] = Field(None, description="Tags for search and organization.")
    log: Optional[LogUpdate] = Field(None, description="Audit log.")


class VisualResourcesRead(VisualResourcesBase):
    """
    Read schema for the visual resources document.
    Complete representation including the document ID.
    """
    id: str = Field(..., description="ObjectId of the visual resource.")
    log: LogRead = Field(..., description="Audit log.")

    model_config = ConfigDict(from_attributes=True)