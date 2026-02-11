from typing import Optional
from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from acb_orm.validations.valid_reference_id import validate_reference_id
from acb_orm.collections.bulletins_version import BulletinsVersion
from acb_orm.enums.outcome_cycle import OutcomeCycle

class ReviewCycleBase(BaseModel):
    """
    Base schema for the review cycle embedded document.
    """
    bulletin_version_id: str = Field(..., description="ID of the bulletin version being reviewed.")
    cycle_number: int = Field(..., description="Sequential number of the review cycle.")
    submitted_at: datetime = Field(..., description="Date and time when the review cycle was submitted.")
    outcome: Optional[OutcomeCycle] = Field(None, description="Outcome of the review: 'approved', 'rejected', or 'pending'.")

class ReviewCycleCreate(ReviewCycleBase):
    """
    Creation schema for a review cycle.
    """
    completed_at: Optional[datetime] = Field(None, description="Date and time when the review was completed.")

    @field_validator('bulletin_version_id')
    def validate_bulletin_version_id(cls, v):
        return validate_reference_id(v, BulletinsVersion)

class ReviewCycleUpdate(BaseModel):
    """
    Update schema for a review cycle.
    """
    completed_at: Optional[datetime] = Field(None, description="Date and time when the review was completed.")
    outcome: Optional[OutcomeCycle] = Field(None, description="Outcome of the review: 'approved', 'rejected', or 'pending'.")

class ReviewCycleRead(ReviewCycleBase):
    """
    Read schema for a review cycle.
    """
    completed_at: Optional[datetime] = Field(None, description="Date and time when the review was completed.")
