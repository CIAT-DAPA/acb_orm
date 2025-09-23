from mongoengine import Document, StringField, ObjectIdField, EmbeddedDocumentField, EmbeddedDocument, DictField, ReferenceField
from acb_orm.auxiliaries.log import Log

class TemplatesVersion(Document):
    """
    This model maps to the 'templates_versions' collection. It stores each
    immutable version of a template, including its complete structure and
    design at a specific point in time.
    """
    meta = {
        'collection': 'templates_versions',
        'indexes': [
            'template_master_id',
            'version_num',
            'previous_version_id'
        ]
    }

    template_master_id = ReferenceField('TemplatesMaster')
    previous_version_id = ReferenceField('self')
    version_num = StringField()
    commit_message = StringField(required=True)
    content = DictField(required=True)
    log = EmbeddedDocumentField(Log)