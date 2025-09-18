from mongoengine import Document, StringField, ObjectIdField, EmbeddedDocumentField, EmbeddedDocument, DictField, ReferenceField
from acb_orm.auxiliaries.log import Log

class TemplatesVersion(Document):
    """
    This model maps to the 'templates_versions' collection. It stores each
    immutable version of a template, including its complete structure and
    design at a specific point in time.
    """
    meta = {'collection': 'templates_versions'}

    template_master_id = ReferenceField('TemplatesMaster')
    version_num = StringField()
    previous_version_id = ReferenceField('self')
    log = EmbeddedDocumentField(Log)
    commit_message = StringField()
    content = DictField(required=True)