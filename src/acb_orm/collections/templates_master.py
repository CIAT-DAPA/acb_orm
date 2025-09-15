from mongoengine import Document, StringField, EmbeddedDocumentField, ReferenceField, EnumField
from acb_orm.auxiliaries.log import Log
from acb_orm.auxiliaries.access_config import AccessConfig
from acb_orm.enums.status_template import StatusTemplate
from acb_orm.collections.templates_version import TemplatesVersion

class TemplatesMaster(Document):
    """
    This model maps to the 'templates_master' collection. It acts as the
    main repository for templates, grouping all their versions and
    high-level metadata.
    """
    meta = {'collection': 'templates_master'}

    template_name = StringField(required=True)
    description = StringField(required=False)
    current_version_id = ReferenceField(TemplatesVersion, required=False)
    status = EnumField(StatusTemplate)
    access_config = EmbeddedDocumentField(AccessConfig, required=True)
    log = EmbeddedDocumentField(Log, required=True)
