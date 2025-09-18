from acb_orm.auxiliaries.access_config import AccessConfig
from acb_orm.enums.access_type import AccessType
from acb_orm.schemas.access_config_schema import AccessConfigCreate, AccessConfigRead

def test_access_config_model():
    access_config = AccessConfig(access_type=AccessType.PUBLIC, allowed_groups=[])
    assert access_config.access_type == AccessType.PUBLIC
    assert access_config.allowed_groups == []

def test_access_config_schema():
    data = {
        "access_type": "public",
        "allowed_groups": []
    }
    schema = AccessConfigCreate(**data)
    assert schema.access_type == AccessType.PUBLIC
    assert schema.allowed_groups == []

    read_schema = AccessConfigRead(**data)
    assert read_schema.access_type == AccessType.PUBLIC
