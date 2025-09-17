from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field, model_validator
from acb_orm.validations.valid_reference_id import ValidReferenceId
from acb_orm.collections import BulletinsVersion, User

class TargetElementSchema(BaseModel):
    """
    Schema for the TargetElement embedded document.
    Links a comment to a specific part of a bulletin.
    """
    section_id: Optional[str] = Field(None, description="ID of the section where the comment is located.")
    block_id: Optional[str] = Field(None, description="ID of the block within the section.")
    field_id: Optional[str] = Field(None, description="ID of the field within the block.")

    @model_validator(mode='after')
    def validate_dependencies(self):
        """
        Validates that if a nested element is provided, its parent elements are also present.
        """
        if self.field_id and not (self.section_id and self.block_id):
            raise ValueError("section_id and block_id must be provided if field_id is present.")
        if self.block_id and not self.section_id:
            raise ValueError("section_id must be provided if block_id is present.")
        return self

class CommentBase(BaseModel):
    """
    Base schema for the Comment embedded document.
    """
    comment_id: Optional[str] = Field(None, description="The unique ID of the comment.")
    text: str = Field(..., description="The content of the comment.")
    created_at: datetime = Field(..., description="The date and time the comment was created.")
    target_element: Optional[TargetElementSchema] = Field(None, description="The specific element in the bulletin the comment is targeting.")
    
class CommentCreate(CommentBase):
    """
    Creation schema for a new Comment.
    """
    bulletin_version_id: ValidReferenceId[BulletinsVersion] = Field(..., description="ID of the bulletin version.")
    author_id: ValidReferenceId[User] = Field(..., description="ID of the user who authored the comment.")

class CommentUpdate(BaseModel):
    """
    Update schema for an existing Comment.
    """
    text: Optional[str] = Field(None, description="The updated content of the comment.")

class CommentReplyUpdate(BaseModel):
    """
    Update schema for adding a reply to a comment.
    """
    replies: List['CommentCreate'] = Field(..., description="The reply comments to be added.")

class CommentRead(CommentBase):
    """
    Read schema for a Comment.
    It includes all fields, including optional ones, to represent the full document.
    """
    bulletin_version_id: str = Field(..., description="ID of the bulletin version.")
    author_id: str = Field(..., description="ID of the user who authored the comment.")
    replies: Optional[List['CommentRead']] = Field(None, description="A list of replies to the comment.")
