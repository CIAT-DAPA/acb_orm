from datetime import datetime
import pytest
from bson import ObjectId
from acb_orm.auxiliaries.log import Log
from acb_orm.schemas.log_schema import LogCreate, LogUpdate, LogRead
from acb_orm.collections.users import User

def test_log_model_creation(setup_db):
    """
    Prueba la creación del modelo Log como EmbeddedDocument.
    """
    user_id = setup_db['user_1']
    user = User.objects.get(id=user_id)
    now = datetime(2023, 1, 1, 0, 0, 0)
    log = Log(created_at=now, creator_user_id=user)
    assert log.created_at == now
    assert log.creator_user_id == user

def test_log_model_update(setup_db):
    """
    Prueba la actualización del modelo Log.
    """
    user_id = setup_db['user_2']
    user = User.objects.get(id=user_id)
    now = datetime(2023, 1, 2, 0, 0, 0)
    log = Log(updated_at=now, updater_user_id=user)
    assert log.updated_at == now
    assert log.updater_user_id == user

def test_log_schema_create(setup_db):
    """
    Prueba el esquema LogCreate de Pydantic.
    """
    now = datetime(2023, 1, 1, 0, 0, 0)
    data = {
        "created_at": now,
        "creator_user_id": setup_db['user_1']
    }
    schema = LogCreate(**data)
    assert schema.created_at == now
    assert schema.creator_user_id == setup_db['user_1']

def test_log_schema_update(setup_db):
    """
    Prueba el esquema LogUpdate de Pydantic.
    """
    now = datetime(2023, 1, 2, 0, 0, 0)
    data = {
        "updated_at": now,
        "updater_user_id": setup_db['user_2']
    }
    schema = LogUpdate(**data)
    assert schema.updated_at == now
    assert schema.updater_user_id == setup_db['user_2']

def test_log_schema_read(setup_db):
    """
    Prueba el esquema LogRead de Pydantic.
    """
    now = datetime(2023, 1, 1, 0, 0, 0)
    data = {
        "created_at": now,
        "creator_user_id": setup_db['user_1'],
        "updated_at": None,
        "updater_user_id": None
    }
    schema = LogRead(**data)
    assert schema.created_at == now
    assert schema.creator_user_id == setup_db['user_1']
    assert schema.updated_at is None
    assert schema.updater_user_id is None

def test_log_schema_read_with_update(setup_db):
    """
    Prueba el esquema LogRead con campos de actualización.
    """
    now = datetime(2023, 1, 1, 0, 0, 0)
    update_now = datetime(2023, 1, 2, 0, 0, 0)
    data = {
        "created_at": now,
        "creator_user_id": setup_db['user_1'],
        "updated_at": update_now,
        "updater_user_id": setup_db['user_2']
    }
    schema = LogRead(**data)
    assert schema.updated_at == update_now
    assert schema.updater_user_id == setup_db['user_2']


