from mongoengine import Document, StringField, ListField, EmbeddedDocumentField, ReferenceField, DictField, EnumField
from acb_orm.auxiliaries.access_config import AccessConfig
from acb_orm.auxiliaries.log import Log
from acb_orm.collections.templates_master import TemplatesMaster
from acb_orm.enums.status_card import StatusCard
from acb_orm.enums.card_type import CardType

class Cards(Document):
    """
    Model for the 'cards' collection.
    Predefined content library for insertion into bulletins.
    """
    meta = {
        'collection': 'cards',
        'indexes': [
            'card_name',
            'card_type',
            'templates_master_ids',
            'tags',
            'status',
            'parent_card_id'
        ]
    }

    card_name = StringField(required=True)
    name_machine = StringField()
    description = StringField()
    templates_master_ids = ListField(ReferenceField(TemplatesMaster))
    access_config = EmbeddedDocumentField(AccessConfig, required=True)
    card_type = EnumField(CardType)
    thumbnail_images = ListField(StringField())
    tags = ListField(StringField())
    parent_card_id = ReferenceField('self')
    status = EnumField(StatusCard)
    content = DictField(required=True)
    log = EmbeddedDocumentField(Log, required=True)
