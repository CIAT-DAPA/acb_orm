from mongoengine import EmbeddedDocument, DateTimeField, ReferenceField
from acb_orm.collections.users import User
from datetime import datetime

class Log(EmbeddedDocument):
    """
    Embedded document to store audit information for each document.
    """
    created_at = DateTimeField(default=datetime.now)
    creator_user_id = ReferenceField(User, required=True)
    updated_at = DateTimeField()
    updater_user_id = ReferenceField(User)