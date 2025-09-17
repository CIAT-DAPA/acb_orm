from mongoengine import EmbeddedDocument, ReferenceField
from acb_orm.collections.users import User
from acb_orm.collections.roles import Role

class UserAccess(EmbeddedDocument):
    """
    Embedded document to define a user's access and role within a group.
    """
    user_id = ReferenceField(User, required=True)
    role_id = ReferenceField(Role, required=True)