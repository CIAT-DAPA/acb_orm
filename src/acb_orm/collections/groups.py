from mongoengine import Document, StringField, ListField, EmbeddedDocumentField
from acb_orm.auxiliaries.log import Log
from acb_orm.auxiliaries.user_access import UserAccess

class Group(Document):
    """
    This model maps to the 'groups' collection. It organizes users by
    affiliation and stores their roles within the group.
    """
    meta = {'collection': 'groups'}

    group_name = StringField(required=True, unique=True)
    country = StringField(required=True)
    description = StringField(required=False)
    users_access = ListField(EmbeddedDocumentField(UserAccess), default=list)
    log = EmbeddedDocumentField(Log, required=True)