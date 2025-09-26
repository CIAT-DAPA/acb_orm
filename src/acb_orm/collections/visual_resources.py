from mongoengine import Document, StringField, ListField, EmbeddedDocumentField, EnumField
from acb_orm.auxiliaries.log import Log
from acb_orm.auxiliaries.access_config import AccessConfig
from acb_orm.enums.status_visual_resource import StatusVisualResource
from acb_orm.enums.file_type import FileType

class VisualResources(Document):
    """
    Model for the 'visual_resources' collection.
    Metadata catalog for visual files stored on the server.
    """
    meta = {'collection': 'visual_resources'}

    file_url = StringField(required=True)
    file_name = StringField(required=True)
    file_type = EnumField(FileType, required=True)
    access_config = EmbeddedDocumentField(AccessConfig)
    status = EnumField(StatusVisualResource)
    log = EmbeddedDocumentField(Log, required=True)
