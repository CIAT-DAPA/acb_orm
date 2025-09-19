from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator
from acb_orm.validations.valid_reference_id import validate_reference_id
from acb_orm.collections.users import User

class LogCreate(BaseModel):
    """
    Creation schema for the log object.
    Only contains fields that are populated on creation.
    """
    created_at: Optional[datetime] = Field(default_factory=datetime.now, description="The date and time the document was created.")
    creator_user_id: str = Field(..., description="The ID of the user who created the document.")

    @field_validator('creator_user_id')
    def validate_creator_user_id(cls, v):
        return validate_reference_id(v, User)

class LogUpdate(BaseModel):
    """
    Update schema for the log object.
    Only contains fields that are modified during an update.
    """
    updated_at: Optional[datetime] = Field(default_factory=datetime.now, description="The date and time the document was last updated.")
    updater_user_id: str = Field(..., description="The ID of the user who last updated the document.")

    @field_validator('updater_user_id')
    def validate_updater_user_id(cls, v):
        return validate_reference_id(v, User)

class LogRead(BaseModel):
    """
    Read schema for the log object.
    It includes all fields, with update fields being optional.
    """
    created_at: datetime = Field(..., description="The date and time the document was created.")
    creator_user_id: str = Field(..., description="The ID of the user who created the document.")
    updated_at: Optional[datetime] = Field(None, description="The date and time the document was last updated.")
    updater_user_id: Optional[str] = Field(None, description="The ID of the user who last updated the document.")