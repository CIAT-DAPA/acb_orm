from mongoengine import Document, StringField, EmbeddedDocumentField, ReferenceField, EnumField
from acb_orm.auxiliaries.log import Log
from acb_orm.auxiliaries.access_config import AccessConfig
from acb_orm.enums.status_bulletin import StatusBulletin
from acb_orm.collections.templates_master import TemplatesMaster
from acb_orm.collections.templates_version import TemplatesVersion
from acb_orm.collections.bulletins_version import BulletinsVersion

class BulletinsMaster(Document):
    """
    This model maps to the 'bulletins_master' collection. It acts as the
    main repository for bulletins, grouping all their versions and
    high-level metadata.
    """
    meta = {'collection': 'bulletins_master'}
    
    bulletin_name = StringField(required=True)
    base_template_master_id = ReferenceField(TemplatesMaster, required=True)
    base_template_version_id = ReferenceField(TemplatesVersion, required=True)
    current_version_id = ReferenceField(BulletinsVersion)
    status = EnumField(StatusBulletin, default=StatusBulletin.DRAFT)
    access_config = EmbeddedDocumentField(AccessConfig, required=True)
    log = EmbeddedDocumentField(Log, required=True)