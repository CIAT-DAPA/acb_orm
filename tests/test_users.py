from datetime import datetime
import pytest
from bson import ObjectId
from pydantic import ValidationError

from acb_orm.collections.users import User
from acb_orm.schemas.users_schema import UsersCreate, UsersUpdate, UsersRead
from acb_orm.auxiliaries.log import Log

# --- PRUEBAS DEL MODELO DE MONGOENGINE ---

def test_create_user_model(db_connection, setup_db):
    log_data = {'created_at': datetime.now(), 'creator_user_id': setup_db['user_1']}
    log = Log(**log_data)
    user = User(
        ext_id="test_ext_id",
        is_active=True,
        log=log
    )
    user.save()
    assert user.id is not None
    assert user.ext_id == "test_ext_id"
    assert user.is_active is True

def test_retrieve_user_document(setup_db):
    user_id = setup_db['user_1']
    retrieved_user = User.objects.get(id=user_id)
    assert retrieved_user is not None
    assert retrieved_user.ext_id == "Test User 1"
    assert retrieved_user.is_active is True

# --- PRUEBAS DE ESQUEMAS DE PYDANTIC ---

def test_create_schema_valid(setup_db):
    data = {
        "ext_id": "test_ext_id",
        "is_active": True,
        "log": {
            "created_at": datetime.now(),
            "creator_user_id": setup_db['user_1']
        }
    }
    schema = UsersCreate(**data)
    assert schema.ext_id == "test_ext_id"
    assert schema.is_active is True
    assert schema.log.creator_user_id == setup_db['user_1']

def test_create_schema_invalid(setup_db):
    data = {
        "is_active": True,
        "log": {
            "created_at": datetime.now(),
            "creator_user_id": setup_db['user_1']
        }
    }
    with pytest.raises(ValidationError):
        UsersCreate(**data)

def test_update_schema_valid(setup_db):
    data = {
        "is_active": False,
        "log": {
            "updated_at": datetime.now(),
            "updater_user_id": setup_db['user_2']
        }
    }
    schema = UsersUpdate(**data)
    assert schema.is_active is False
    assert schema.log.updater_user_id == setup_db['user_2']

def test_read_schema_valid(setup_db):
    data = {
        "id": setup_db['user_1'],
        "ext_id": "Test User 1",
        "is_active": True,
        "log": {
            "created_at": datetime.now(),
            "creator_user_id": setup_db['user_1']
        }
    }
    schema = UsersRead(**data)
    assert schema.id == data["id"]
    assert schema.ext_id == "Test User 1"
    assert schema.is_active is True
    assert schema.log.creator_user_id == setup_db['user_1']

def test_read_schema_invalid(setup_db):
    data = {
        "ext_id": "Test User 1",
        "is_active": True,
        "log": {
            "created_at": datetime.now(),
            "creator_user_id": setup_db['user_1']
        }
    }
    with pytest.raises(ValidationError):
        UsersRead(**data)
