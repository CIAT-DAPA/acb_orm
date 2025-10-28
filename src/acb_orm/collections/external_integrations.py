from mongoengine import Document, StringField, EmbeddedDocumentField, EnumField, ListField, DateTimeField, DictField
from acb_orm.auxiliaries.log import Log
from acb_orm.auxiliaries.access_config import AccessConfig
from acb_orm.enums.integration_service_type import IntegrationServiceType
from acb_orm.enums.integration_status import IntegrationStatus
from acb_orm.enums.auth_type import AuthType

class ExternalIntegration(Document):
    """
    Collection: external_integrations
    Stores configuration to connect with external APIs/services.
    Credentials should be stored as secret_ref (preferred) or encrypted (if used).
    """
    meta = {
        'collection': 'external_integrations',
        'indexes': [
            {'fields': ['name'], 'unique': True},
            'service_type',
            'status'
        ]
    }

    name = StringField(required=True, unique=True)
    description = StringField()
    service_type = EnumField(IntegrationServiceType, required=True)
    base_url = StringField(required=True)
    auth_type = EnumField(AuthType, default=AuthType.NONE)
    # Prefer storing secret reference (secret_id) instead of raw credentials
    secret_ref = StringField()          # reference to external secret manager (recommended)
    auth_config = DictField()           # optional: non-sensitive config (e.g., scopes, header names)
    status = EnumField(IntegrationStatus, default=IntegrationStatus.ACTIVE)
    access_config = EmbeddedDocumentField(AccessConfig)
    tags = ListField(StringField(), default=list)
    last_checked = DateTimeField()
    last_error = StringField()
    metadata = DictField()              # free-form provider metadata
    log = EmbeddedDocumentField(Log, required=True)
