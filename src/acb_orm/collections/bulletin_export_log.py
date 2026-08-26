# acb_orm/models/bulletin_export_log.py
from mongoengine import Document, StringField, EmbeddedDocumentField, ReferenceField, DateTimeField, EnumField
from datetime import datetime, timezone
from acb_orm.enums.export_format import ExportFormat

class BulletinExportLog(Document):
    """
    Maps to 'bulletin_export_logs' collection. Records every export action
    performed on a bulletin version.
    """
    meta = {
        'collection': 'bulletin_export_logs',
        'indexes': [
            'user_id',
            'bulletin_master_id',
            'bulletin_version_id',
            'exported_at'
        ]
    }

    user_id = ReferenceField('User', required=True)
    bulletin_master_id  = ReferenceField('BulletinsMaster', required=True)
    bulletin_version_id = ReferenceField('BulletinsVersion', required=True)
    bulletin_title  = StringField()         
    format = EnumField(ExportFormat, required=True)
    exported_at = DateTimeField(default=lambda: datetime.now(timezone.utc))