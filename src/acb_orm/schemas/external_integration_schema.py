from typing import Optional, List, Dict
from pydantic import BaseModel, Field, HttpUrl, model_validator
from acb_orm.enums.integration_service_type import IntegrationServiceType
from acb_orm.enums.integration_status import IntegrationStatus
from acb_orm.enums.auth_type import AuthType
from acb_orm.schemas.access_config_schema import AccessConfigCreate, AccessConfigRead
from acb_orm.schemas.log_schema import LogCreate, LogRead

class ExternalIntegrationBase(BaseModel):
    name: str = Field(..., description="Integration name")
    description: Optional[str] = Field(None, description="Short description")
    service_type: IntegrationServiceType = Field(..., description="Type of service")
    base_url: HttpUrl = Field(..., description="Base URL / endpoint")
    auth_type: AuthType = Field(AuthType.NONE, description="Authentication mechanism")
    # secret_ref: prefer keeping credential reference instead of raw secrets
    secret_ref: Optional[str] = Field(None, description="Reference id in secret manager")
    auth_config: Optional[Dict[str, str]] = Field(None, description="Non-sensitive auth params")
    status: Optional[IntegrationStatus] = Field(IntegrationStatus.ACTIVE)
    tags: Optional[List[str]] = Field(None)

class ExternalIntegrationCreate(ExternalIntegrationBase):
    access_config: AccessConfigCreate = Field(..., description="Access configuration")
    log: Optional[LogCreate] = Field(None, description="Audit log")

    @model_validator(mode='after')
    def validate_secret_or_auth(self, values):
        # If auth_type != NONE, require secret_ref or auth_config to be present
        if values.get('auth_type') != AuthType.NONE and not (values.get('secret_ref') or values.get('auth_config')):
            raise ValueError("auth_type requires secret_ref or auth_config")
        return values

class ExternalIntegrationUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    base_url: Optional[HttpUrl]
    auth_type: Optional[AuthType]
    secret_ref: Optional[str]
    auth_config: Optional[Dict[str, str]]
    status: Optional[IntegrationStatus]
    access_config: Optional[AccessConfigCreate]
    tags: Optional[List[str]]
    log: Optional[LogRead]

class ExternalIntegrationRead(ExternalIntegrationBase):
    id: str
    access_config: AccessConfigRead
    log: LogRead
    model_config = {"from_attributes": True}
