from typing import Optional, List, Any
from pydantic import BaseModel, Field, ConfigDict, field_validator
from acb_orm.schemas.log_schema import LogCreate, LogRead, LogUpdate
from acb_orm.schemas.comment_schema import CommentCreate, CommentRead, CommentUpdate
from acb_orm.schemas.review_cycle_schema import ReviewCycleCreate, ReviewCycleRead, ReviewCycleUpdate
from acb_orm.collections.bulletins_master import BulletinsMaster
from acb_orm.collections.users import User
from acb_orm.validations.valid_reference_id import validate_reference_id
from datetime import datetime

class BulletinReviewsBase(BaseModel):
    """
    Base schema for the bulletin reviews document.
    """
    bulletin_master_id: str = Field(..., description="ID of the bulletin master document.")
    review_cycles: List[ReviewCycleCreate] = Field(default=[], description="Array of review cycles.")

class BulletinReviewsCreate(BulletinReviewsBase):
    """
    Creation schema for the bulletin reviews document.
    All fields are required for creating a new document.
    """
    reviewer_user_id: Optional[str] = Field(None, description="ID of the user who is reviewing the bulletin.")
    log: Optional[LogCreate] = Field(None, description="Audit log.")
    comments: List[CommentCreate] = Field(default=[], description="Array of comments.")

    @field_validator('bulletin_master_id')
    def validate_bulletin_master_id(cls, v):
        return validate_reference_id(v, BulletinsMaster)

    @field_validator('reviewer_user_id')
    def validate_reviewer_user_id(cls, v):
        return validate_reference_id(v, User)

class BulletinReviewsUpdate(BaseModel):
    """
    Update schema for the bulletin reviews document.
    The log and comments will be handled by the service layer.
    """
    log: Optional[LogUpdate] = Field(None, description="Audit log.")
    review_cycles: Optional[List[ReviewCycleCreate]] = Field(None, description="Array of review cycles.")
    comments: Optional[List[CommentCreate]] = Field(None, description="Array of comments.")

class BulletinReviewsRead(BulletinReviewsBase):
    """
    Read schema for the bulletin reviews document.
    Complete representation including the document ID.
    """
    id: str = Field(..., description="ObjectId of the bulletin review document.")
    reviewer_user_id: Optional[str] = Field(None, description="ID of the user who reviewed the bulletin.")
    reviewer_first_name: Optional[str] = Field(None, description="First name of the reviewer.")
    reviewer_last_name: Optional[str] = Field(None, description="Last name of the reviewer.")
    log: LogRead = Field(..., description="Audit log.")
    comments: List[CommentRead] = Field(default=[], description="Array of comments.")
    model_config = ConfigDict(from_attributes=True)