from enum import Enum

class StatusBulletin(Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"
    REVIEW = "review"
    PENDING_REVIEW = "pending_review"
    REJECTED = "rejected"