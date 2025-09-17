from typing import Optional, List, Any, Dict
from pydantic import BaseModel, Field, ConfigDict
from acb_orm.schemas.log_schema import LogCreate, LogRead, LogUpdate
from acb_orm.schemas.access_config_schema import AccessConfigCreate, AccessConfigRead, AccessConfigUpdate
from acb_orm.collections.templates_master import TemplatesMaster
from acb_orm.validations.valid_reference_id import ValidReferenceId

class CardsBase(BaseModel):
    """
    Base schema for the cards document.
    Contains common fields for creation and reading.
    """
    card_name: str = Field(..., description="Name of the card.")
    card_type: str = Field(..., description="Type of the card (e.g., 'pest_or_disease').")

class CardsCreate(CardsBase):
    """
    Creation schema for the cards document.
    All fields are required when creating a new document.
    """
    templates_master_ids: List[ValidReferenceId[TemplatesMaster]] = Field(..., description="List of IDs of compatible template masters.")
    access_config: AccessConfigCreate = Field(..., description="Access configuration.")
    content: Dict[str, Any] = Field(..., description="Flexible content structure of the card.")
    log: LogCreate = Field(..., description="Audit log.")
    
class CardsUpdate(BaseModel):
    """
    Update schema for the cards document.
    The log will be handled by the service layer.
    """
    card_name: Optional[str] = Field(None, description="Name of the card.")
    card_type: Optional[str] = Field(None, description="Type of the card.")
    templates_master_ids: Optional[List[ValidReferenceId[TemplatesMaster]]] = Field(None, description="List of IDs of compatible template masters.")
    access_config: Optional[AccessConfigUpdate] = Field(None, description="Access configuration.")
    log: Optional[LogUpdate] = Field(..., description="Audit log.")
    content: Optional[Dict[str, Any]] = Field(None, description="Flexible content structure of the card.")

class CardsRead(CardsBase):
    """
    Read schema for the cards document.
    Complete representation including the document ID.
    """
    id: str = Field(..., description="ObjectId of the card.")
    templates_master_ids: List[str] = Field(..., description="List of IDs of compatible template masters.")
    access_config: AccessConfigRead = Field(..., description="Access configuration.")
    content: Dict[str, Any] = Field(..., description="Flexible content structure of the card.")
    log: LogRead = Field(..., description="Audit log.")
    model_config = ConfigDict(from_attributes=True)