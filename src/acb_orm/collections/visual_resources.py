from mongoengine import Document, StringField, ListField, EmbeddedDocumentField
from acb_orm.auxiliaries.log import Log

class VisualResources(Document):
    """
    Model for the 'visual_resources' collection.
    Metadata catalog for visual files stored on the server.
    """
    meta = {'collection': 'visual_resources'}

    file_url = StringField(required=True)
    file_name = StringField(required=True)
    file_type = StringField(required=True)
    tags = ListField(StringField(), required=False)
    log = EmbeddedDocumentField(Log, required=True)
