from mongoengine import Document, StringField, ListField, EmbeddedDocumentField, ReferenceField, DictField
from acb_orm.auxiliaries.access_config import AccessConfig
from acb_orm.auxiliaries.log import Log
from acb_orm.collections.templates_master import TemplatesMaster

class Cards(Document):
    """
    Model for the 'cards' collection.
    Predefined content library for insertion into bulletins.
    """
    meta = {'collection': 'cards'}

    card_name = StringField(required=True)
    card_type = StringField(required=True)
    templates_master_ids = ListField(ReferenceField(TemplatesMaster), required=True)
    access_config = EmbeddedDocumentField(AccessConfig, required=True)
    content = DictField(required=True)
    log = EmbeddedDocumentField(Log, required=True)
