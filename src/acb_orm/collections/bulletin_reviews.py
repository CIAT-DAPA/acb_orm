from mongoengine import Document, DateTimeField, EmbeddedDocumentField, ReferenceField, ListField
from acb_orm.auxiliaries.log import Log
from acb_orm.auxiliaries.comment import Comment  # <-- Importa el modelo Comment

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
            'completed_at'
        ]
    }

    bulletin_master_id = ReferenceField('BulletinsMaster', required=True)
    reviewer_user_id = ReferenceField('User', required=True)
    log = EmbeddedDocumentField(Log, required=True)
    completed_at = DateTimeField()
    comments = ListField(EmbeddedDocumentField(Comment))