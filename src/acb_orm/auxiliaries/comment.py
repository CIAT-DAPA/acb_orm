from mongoengine import EmbeddedDocument, ReferenceField, StringField, DateTimeField, ListField, EmbeddedDocumentField, ObjectIdField
from acb_orm.collections.users import User
from acb_orm.collections.bulletins_version import BulletinVersion
from acb_orm.auxiliaries.target_element import TargetElement
from datetime import datetime

class Comment(EmbeddedDocument):
    """
    Embedded document to store comments and their replies on bulletin reviews.
    This model is recursive to allow for comment threads.
    """
    # Using StringField to match the example JSON
    comment_id = StringField()
    bulletin_version_id = ReferenceField(BulletinVersion, required=True)
    text = StringField(required=True)
    author_id = ReferenceField(User, required=True)
    created_at = DateTimeField(required=True, default=datetime.now())
    # This field is optional as per documentation
    target_element = EmbeddedDocumentField(TargetElement)
    replies = ListField(EmbeddedDocumentField('self'), default=list)