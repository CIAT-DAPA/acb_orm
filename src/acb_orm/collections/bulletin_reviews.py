from mongoengine import Document, EmbeddedDocumentField, ReferenceField, ListField
from acb_orm.auxiliaries.log import Log
from acb_orm.auxiliaries.comment import Comment  
from acb_orm.auxiliaries.review_cycle import ReviewCycle 

class BulletinReviews(Document):
    """
    This model maps to the 'bulletin_reviews' collection. It records each
    review cycle for a bulletin, including comments and completion status.
    """
    meta = {
        'collection': 'bulletin_reviews',
        'indexes': [
            'bulletin_master_id',
            'reviewer_user_id',
        ]
    }

    bulletin_master_id = ReferenceField('BulletinsMaster', required=True)
    reviewer_user_id = ReferenceField('User')
    log = EmbeddedDocumentField(Log, required=True)
    review_cycles = ListField(EmbeddedDocumentField(ReviewCycle), default=list)
    comments = ListField(EmbeddedDocumentField(Comment), default=list)