from mongoengine import EmbeddedDocument, DateTimeField, ReferenceField
from acb_orm.collections.users import User
from datetime import datetime

class Log(EmbeddedDocument):
    """
    Embedded document to store audit information for each document.
    """
    created_at = DateTimeField(required=True, default=datetime.now())
    creator_user_id = ReferenceField(User, required=True)
    updated_at = DateTimeField(required=False)
    updater_user_id = ReferenceField(User, required=False)

    def save(self, *args, **kwargs):
        self.updated_at = datetime.now()
        return super(Log, self).save(*args, **kwargs)