from datetime import datetime
import pytest
from bson import ObjectId
from pydantic import ValidationError

from acb_orm.auxiliaries.user_access import UserAccess
from acb_orm.schemas.user_access_schema import UserAccessCreate, UserAccessUpdate, UserAccessRead
from acb_orm.collections.users import User
from acb_orm.collections.roles import Role

def test_create_user_access_model(db_connection, setup_db):
    user = User.objects.get(id=setup_db['user_1'])
    role = Role.objects.get(id=setup_db['role_admin'])
    user_access = UserAccess(user_id=user, role_id=role)
    assert user_access.user_id == user
    assert user_access.role_id == role

def test_create_schema_valid(setup_db):
    data = {
        "user_id": setup_db['user_1'],
        "role_id": setup_db['role_admin']
    }
    schema = UserAccessCreate(**data)
    assert schema.user_id == setup_db['user_1']
    assert schema.role_id == setup_db['role_admin']

def test_create_schema_invalid(setup_db):
    data = {
        "role_id": setup_db['role_admin']
    }
    with pytest.raises(ValidationError):
        UserAccessCreate(**data)

def test_update_schema_valid(setup_db):
    data = {
        "user_id": setup_db['user_2'],
        "role_id": setup_db['role_editor']
    }
    schema = UserAccessUpdate(**data)
    assert schema.user_id == setup_db['user_2']
    assert schema.role_id == setup_db['role_editor']

def test_read_schema_valid(setup_db):
    data = {
        "user_id": setup_db['user_1'],
        "role_id": setup_db['role_admin']
    }
    schema = UserAccessRead(**data)
    assert schema.user_id == setup_db['user_1']
    assert schema.role_id == setup_db['role_admin']

def test_read_schema_invalid(setup_db):
    data = {
        "role_id": setup_db['role_admin']
    }
    with pytest.raises(ValidationError):
        UserAccessRead(**data)
