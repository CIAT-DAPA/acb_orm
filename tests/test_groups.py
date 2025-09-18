from datetime import datetime
import pytest
from bson import ObjectId
from pydantic import ValidationError

from acb_orm.collections.groups import Group
from acb_orm.auxiliaries.user_access import UserAccess
from acb_orm.schemas.groups_schema import GroupsCreate, GroupsUpdate, GroupsRead
from acb_orm.auxiliaries.log import Log

def test_create_group_model(db_connection, setup_db):
    log_data = {'created_at': datetime.now(), 'creator_user_id': setup_db['user_1']}
    log = Log(**log_data)
    user_access = UserAccess(user_id=setup_db['user_1'], role_id=setup_db['role_admin'])
    group = Group(
        group_name="Test Group",
        country="Colombia",
        description="Grupo de prueba",
        users_access=[user_access],
        log=log
    )
    group.save()
    assert group.id is not None
    assert group.group_name == "Test Group"
    assert group.country == "Colombia"
    assert len(group.users_access) == 1

def test_retrieve_group_document(setup_db):
    log_data = {'created_at': datetime.now(), 'creator_user_id': setup_db['user_1']}
    log = Log(**log_data)
    user_access = UserAccess(user_id=setup_db['user_1'], role_id=setup_db['role_admin'])
    group = Group(
        group_name="Grupo Recuperado",
        country="México",
        description="Grupo para recuperar",
        users_access=[user_access],
        log=log
    )
    group.save()
    retrieved_group = Group.objects.get(group_name="Grupo Recuperado")
    assert retrieved_group is not None
    assert retrieved_group.country == "México"
    assert retrieved_group.description == "Grupo para recuperar"

def test_create_schema_valid(setup_db):
    data = {
        "group_name": "Test Group",
        "country": "Colombia",
        "description": "Grupo de prueba",
        "users_access": [
            {
                "user_id": setup_db['user_1'],
                "role_id": setup_db['role_admin']
            }
        ],
        "log": {
            "created_at": datetime.now(),
            "creator_user_id": setup_db['user_1']
        }
    }
    schema = GroupsCreate(**data)
    assert schema.group_name == "Test Group"
    assert schema.country == "Colombia"
    assert len(schema.users_access) == 1

def test_create_schema_invalid(setup_db):
    data = {
        "country": "Colombia",
        "description": "Grupo sin nombre",
        "users_access": [],
        "log": {
            "created_at": datetime.now(),
            "creator_user_id": setup_db['user_1']
        }
    }
    with pytest.raises(ValidationError):
        GroupsCreate(**data)

def test_update_schema_valid(setup_db):
    data = {
        "description": "Descripción actualizada",
        "users_access": [
            {
                "user_id": setup_db['user_2'],
                "role_id": setup_db['role_editor']
            }
        ],
        "log": {
            "updated_at": datetime.now(),
            "updater_user_id": setup_db['user_2']
        }
    }
    schema = GroupsUpdate(**data)
    assert schema.description == "Descripción actualizada"
    assert len(schema.users_access) == 1

def test_read_schema_valid(setup_db):
    data = {
        "id": str(ObjectId()),
        "group_name": "Test Group",
        "country": "Colombia",
        "description": "Grupo de prueba",
        "users_access": [
            {
                "user_id": setup_db['user_1'],
                "role_id": setup_db['role_admin']
            }
        ],
        "log": {
            "created_at": datetime.now(),
            "creator_user_id": setup_db['user_1']
        }
    }
    schema = GroupsRead(**data)
    assert schema.id == data["id"]
    assert schema.group_name == "Test Group"
    assert schema.country == "Colombia"
    assert len(schema.users_access) == 1

def test_read_schema_invalid(setup_db):
    data = {
        "country": "Colombia",
        "description": "Grupo sin nombre",
        "users_access": [],
        "log": {
            "created_at": datetime.now(),
            "creator_user_id": setup_db['user_1']
        }
    }
    with pytest.raises(ValidationError):
        GroupsRead(**data)
