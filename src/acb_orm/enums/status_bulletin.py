from enum import Enum

class StatusBulletin(Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"
    PENDING_REVIEW = "pending_review"
    REJECTED = "rejected"