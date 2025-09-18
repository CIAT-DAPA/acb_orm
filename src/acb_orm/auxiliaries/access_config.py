from mongoengine import EmbeddedDocument, ListField, ReferenceField, EnumField
from acb_orm.enums.access_type import AccessType

class AccessConfig(EmbeddedDocument):
    """
    Embedded document to define access and visibility settings.
    """
    access_type = EnumField(AccessType, default = AccessType.PUBLIC, required=True)
    allowed_groups = ListField(ReferenceField('Group'), default=list)