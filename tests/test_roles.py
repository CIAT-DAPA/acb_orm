from datetime import datetime
import pytest
from bson import ObjectId
from pydantic import ValidationError

from acb_orm.collections.roles import Role
from acb_orm.schemas.roles_schema import RolesCreate, RolesUpdate, RolesRead
from acb_orm.auxiliaries.log import Log

# --- PRUEBAS DEL MODELO DE MONGOENGINE ---

def test_create_role_model(db_connection, setup_db):
    log_data = {'created_at': datetime.now(), 'creator_user_id': setup_db['user_1']}
    log = Log(**log_data)
    role = Role(
        role_name="admin 123",
        description="Administrador del sistema",
        permissions={"manage_users": True, "edit_content": True},
        log=log
    )
    role.save()
    assert role.id is not None
    assert role.role_name == "admin 123"
    assert role.permissions["manage_users"] is True

def test_retrieve_role_document(db_connection, setup_db):
  
    retrieved_role = Role.objects.get(id=setup_db['role_editor'])
    assert retrieved_role is not None
    assert retrieved_role.role_name == "editor"
    assert retrieved_role.permissions["edit_content"] is True

def test_unique_role_document(db_connection, setup_db):
    log_data = {'created_at': datetime.now(), 'creator_user_id': setup_db['user_1']}
    log = Log(**log_data)
    role = Role(
        role_name="editor",
        description="Editor de contenido",
        permissions={"edit_content": True},
        log=log
    )
    with pytest.raises(Exception):
        role.save()

def test_retrieve_role_document(db_connection, setup_db):
    log_data = {'created_at': datetime.now(), 'creator_user_id': setup_db['user_1']}
    log = Log(**log_data)
    role = Role(
        role_name="editor 123",
        description="Editor de contenido",
        permissions={"edit_content": True},
        log=log
    )
    role.save()
    retrieved_role = Role.objects.get(role_name="editor 123")
    assert retrieved_role is not None
    assert retrieved_role.role_name == "editor 123"
    assert retrieved_role.permissions["edit_content"] is True


# --- PRUEBAS DE ESQUEMAS DE PYDANTIC ---

def test_create_schema_valid(setup_db):
    data = {
        "role_name": "admin",
        "description": "Administrador del sistema",
        "permissions": {"manage_users": True, "edit_content": True},
        "log": {
            "created_at": datetime.now(),
            "creator_user_id": setup_db['user_1']
        }
    }
    schema = RolesCreate(**data)
    assert schema.role_name == "admin"
    assert schema.permissions["manage_users"] is True

def test_create_schema_invalid(setup_db):
    data = {
        "description": "Sin nombre",
        "permissions": {"manage_users": True},
        "log": {
            "created_at": datetime.now(),
            "creator_user_id": setup_db['user_1']
        }
    }
    with pytest.raises(ValidationError):
        RolesCreate(**data)

def test_update_schema_valid(setup_db):
    data = {
        "role_name": "editor",
        "description": "Editor actualizado",
        "permissions": {"edit_content": True, "publish": True},
        "log": {
            "updated_at": datetime.now(),
            "updater_user_id": setup_db['user_2']
        }
    }
    schema = RolesUpdate(**data)
    assert schema.role_name == "editor"
    assert schema.permissions["publish"] is True
    assert schema.log.updater_user_id == setup_db['user_2']

def test_read_schema_valid(setup_db):
    data = {
        "id": str(ObjectId()),
        "role_name": "admin",
        "description": "Administrador del sistema",
        "permissions": {"manage_users": True, "edit_content": True},
        "log": {
            "created_at": datetime.now(),
            "creator_user_id": setup_db['user_1']
        }
    }
    schema = RolesRead(**data)
    assert schema.id == data["id"]
    assert schema.role_name == "admin"
    assert schema.permissions["manage_users"] is True
    assert schema.log.creator_user_id == setup_db['user_1']

def test_read_schema_invalid(setup_db):
    data = {
        "role_name": "admin",
        "description": "Administrador del sistema",
        "permissions": {"manage_users": True, "edit_content": True},
        "log": {
            "created_at": datetime.now(),
            "creator_user_id": setup_db['user_1']
        }
    }
    with pytest.raises(ValidationError):
        RolesRead(**data)
