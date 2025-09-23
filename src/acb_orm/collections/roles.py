from mongoengine import Document, StringField, DictField, EmbeddedDocumentField

class Role(Document):
    """
    This model maps to the 'roles' collection. It defines the different
    roles available in the system and their associated permissions.
    """
    meta = {
        'collection': 'roles',
        'indexes': [
            {'fields': ['role_name'], 'unique': True}
        ]
    }

    role_name = StringField(required=True, unique=True)
    description = StringField(required=False)
    permissions = DictField()
    log = EmbeddedDocumentField('Log', required=True)