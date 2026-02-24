from enum import Enum

class OutcomeCycle(Enum):
    APPROVED = "approved"
    CANCELLED = "cancelled"
    PENDING = "pending"
    REJECTED = "rejected"