from mongoengine import Document, StringField, EmbeddedDocumentField, ReferenceField, EnumField, DictField
from acb_orm.auxiliaries.log import Log

class BulletinsVersion(Document):
    """
    This model maps to the 'bulletins_versions' collection. It stores each
    immutable version of a bulletin, with the specific data entered by the
    user.
    """
    meta = {'collection': 'bulletins_versions'}

    bulletin_master_id = ReferenceField('BulletinsMaster', required=True)
    version_num = StringField(required=True)
    previous_version_id = ReferenceField('self')
    log = EmbeddedDocumentField(Log, required=True)
    data = DictField(required=True)
