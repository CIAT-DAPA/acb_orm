from mongoengine import Document, StringField, BooleanField, EmbeddedDocumentField
from acb_orm.auxiliaries.log import Log

class User(Document):
    """
    This model maps to the 'users' collection. It stores user information
    and a link to an external ID.
    """
    meta = {'collection': 'users'}
    
    ext_id = StringField(required=True, unique=True)
    is_active = BooleanField(default=True)
    log = EmbeddedDocumentField(Log, required=True)