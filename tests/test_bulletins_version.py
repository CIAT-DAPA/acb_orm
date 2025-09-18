from datetime import datetime
import pytest
from bson import ObjectId
from pydantic import ValidationError

from acb_orm.collections.bulletins_version import BulletinsVersion
from acb_orm.schemas.bulletins_version_schema import BulletinsVersionCreate, BulletinsVersionRead, BulletinsVersionUpdate
from acb_orm.auxiliaries.log import Log

@pytest.fixture
def non_existent_master_id():
    return str(ObjectId())

@pytest.fixture
def non_existent_version_id():
    return str(ObjectId())

# --- PRUEBAS DEL MODELO DE MONGOENGINE ---

def test_create_bulletins_version_model(db_connection, setup_db):
    log_data = {'created_at': datetime.now(), 'creator_user_id': setup_db['user_1']}
    log = Log(**log_data)
    bulletin_version = BulletinsVersion(
        bulletin_master_id=ObjectId(setup_db['bulletin_master']),
        version_num="2.0",
        previous_version_id=None,
        log=log,
        data={"campo": "nuevo valor"}
    )
    bulletin_version.save()
    assert bulletin_version.id is not None
    assert bulletin_version.version_num == "2.0"

def test_retrieve_bulletins_version_document(setup_db):
    bulletin_version_id = setup_db['bulletin_version']
    retrieved_version = BulletinsVersion.objects.get(id=bulletin_version_id)
    assert retrieved_version is not None
    assert retrieved_version.version_num == "1.0"
    assert "campo" in retrieved_version.data

# --- PRUEBAS DE ESQUEMAS DE PYDANTIC ---

def test_create_schema_valid(setup_db):
    data = {
        "bulletin_master_id": setup_db['bulletin_master'],
        "version_num": "2.0",
        "previous_version_id": None,
        "data": {"campo": "nuevo valor"},
        "log": {
            "created_at": datetime.now(),
            "creator_user_id": setup_db['user_1']
        }
    }
    schema = BulletinsVersionCreate(**data)
    assert schema.version_num == "2.0"
    assert schema.bulletin_master_id == data["bulletin_master_id"]

def test_create_schema_invalid_reference(non_existent_master_id, setup_db):
    data = {
        "bulletin_master_id": non_existent_master_id,
        "version_num": "2.0",
        "previous_version_id": None,
        "data": {"campo": "nuevo valor"},
        "log": {
            "created_at": datetime.now(),
            "creator_user_id": setup_db['user_1']
        }
    }
    with pytest.raises(ValidationError):
        BulletinsVersionCreate(**data)

def test_update_schema_valid(setup_db):
    data = {
        "bulletin_master_id": setup_db['bulletin_master'],
        "previous_version_id": setup_db['bulletin_version'],
        "data": {"campo": "actualizado"},
        "log": {
            "updated_at": datetime.now(),
            "updater_user_id": setup_db['user_2']
        }
    }
    schema = BulletinsVersionUpdate(**data)
    assert schema.data == {"campo": "actualizado"}

def test_update_schema_invalid_reference(non_existent_version_id, setup_db):
    data = {
        "bulletin_master_id": setup_db['bulletin_master'],
        "previous_version_id": non_existent_version_id,
        "data": {"campo": "actualizado"},
        "log": {
            "updated_at": datetime.now(),
            "updater_user_id": setup_db['user_2']
        }
    }
    with pytest.raises(ValidationError):
        BulletinsVersionUpdate(**data)

def test_read_schema_valid(setup_db):
    data = {
        "id": setup_db['bulletin_version'],
        "bulletin_master_id": setup_db['bulletin_master'],
        "version_num": "1.0",
        "previous_version_id": None,
        "data": {"campo": "valor"},
        "log": {
            "created_at": datetime.now(),
            "creator_user_id": setup_db['user_1']
        }
    }
    schema = BulletinsVersionRead(**data)
    assert schema.id == data['id']
    assert schema.version_num == "1.0"
    assert schema.data == {"campo": "valor"}
