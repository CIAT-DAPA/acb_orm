from mongoengine import Document, StringField, EmbeddedDocumentField, ReferenceField, EnumField
from acb_orm.auxiliaries.log import Log
from acb_orm.auxiliaries.access_config import AccessConfig
from acb_orm.enums.status_template import StatusTemplate

class TemplatesMaster(Document):
    """
    This model maps to the 'templates_master' collection. It acts as the
    main repository for templates, grouping all their versions and
    high-level metadata.
    """
    meta = {
        'collection': 'templates_master',
        'indexes': [
            {'fields': ['template_name'], 'unique': True},
            'current_version_id'
        ]
    }

    template_name = StringField(required=True)
    description = StringField()
    current_version_id = ReferenceField('TemplatesVersion')
    status = EnumField(StatusTemplate)
    access_config = EmbeddedDocumentField(AccessConfig)
    log = EmbeddedDocumentField(Log)
