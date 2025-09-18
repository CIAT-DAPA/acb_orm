from datetime import datetime
import pytest
from bson import ObjectId
from pydantic import ValidationError

from acb_orm.collections.bulletins_master import BulletinsMaster
from acb_orm.schemas.bulletins_master_schema import BulletinsMasterCreate, BulletinsMasterRead, BulletinsMasterUpdate
from acb_orm.auxiliaries.log import Log
from acb_orm.auxiliaries.access_config import AccessConfig
from acb_orm.enums.status_bulletin import StatusBulletin

@pytest.fixture
def non_existent_template_id():
    return str(ObjectId())

@pytest.fixture
def non_existent_version_id():
    return str(ObjectId())

# --- PRUEBAS DEL MODELO DE MONGOENGINE ---

def test_create_bulletins_master_model(db_connection, setup_db):
    log_data = {'created_at': datetime.now(), 'creator_user_id': setup_db['user_1']}
    log = Log(**log_data)
    access_config = AccessConfig(access_type='public', allowed_groups=[])
    bulletin = BulletinsMaster(
        bulletin_name="Test Bulletin",
        base_template_master_id=ObjectId(setup_db['template_master']),
        base_template_version_id=ObjectId(setup_db['template_version']),
        current_version_id=None,
        status=StatusBulletin.DRAFT,
        access_config=access_config,
        log=log
    )
    bulletin.save()
    assert bulletin.id is not None
    assert bulletin.bulletin_name == "Test Bulletin"

def test_retrieve_bulletins_master_document(setup_db):
    bulletin_master_id = setup_db['bulletin_master']
    retrieved_bulletin = BulletinsMaster.objects.get(id=bulletin_master_id)
    assert retrieved_bulletin is not None
    assert retrieved_bulletin.bulletin_name == "Ejemplo Bulletin"

# --- PRUEBAS DE ESQUEMAS DE PYDANTIC ---

def test_create_schema_valid(setup_db):
    data = {
        "bulletin_name": "Test Bulletin",
        "status": "draft",
        "base_template_master_id": setup_db['template_master'],
        "base_template_version_id": setup_db['template_version'],
        "current_version_id": None,
        "access_config": {
            "access_type": "public",
        },
        "log": {
            "created_at": datetime.now(),
            "creator_user_id": setup_db['user_1']
        }
    }
    schema = BulletinsMasterCreate(**data)
    assert schema.bulletin_name == "Test Bulletin"
    assert schema.status == StatusBulletin.DRAFT

def test_create_schema_invalid_reference(non_existent_template_id, setup_db):
    data = {
        "bulletin_name": "Test Bulletin",
        "status": "draft",
        "base_template_master_id": non_existent_template_id,
        "base_template_version_id": setup_db['template_version'],
        "current_version_id": None,
        "access_config": {
            "access_type": "public",
        },
        "log": {
            "created_at": datetime.now(),
            "creator_user_id": setup_db['user_1']
        }
    }
    with pytest.raises(ValidationError):
        BulletinsMasterCreate(**data)

def test_update_schema_valid(setup_db):
    data = {
        "bulletin_name": "Updated Bulletin",
        "status": "published",
        "base_template_master_id": setup_db['template_master'],
        "base_template_version_id": setup_db['template_version'],
        "current_version_id": setup_db['bulletin_version'],
        "access_config": None,
        "log": {
            "updated_at": datetime.now(),
            "updater_user_id": setup_db['user_2']
        }
    }
    schema = BulletinsMasterUpdate(**data)
    assert schema.bulletin_name == "Updated Bulletin"

def test_update_schema_invalid_reference(non_existent_version_id, setup_db):
    data = {
        "bulletin_name": "Updated Bulletin",
        "status": "draft",
        "base_template_master_id": setup_db['template_master'],
        "base_template_version_id": setup_db['template_version'],
        "current_version_id": non_existent_version_id,
        "access_config": None,
        "log": {
            "updated_at": datetime.now(),
            "updater_user_id": setup_db['user_2']
        }
    }
    with pytest.raises(ValidationError):
        BulletinsMasterUpdate(**data)

def test_read_schema(setup_db):
    data = {
        "id": setup_db['bulletin_master'],
        "bulletin_name": "Test Bulletin",
        "status": "draft",
        "base_template_master_id": setup_db['template_master'],
        "base_template_version_id": setup_db['template_version'],
        "current_version_id": setup_db['bulletin_version'],
        "access_config": {
            "access_type": "public",
        },
        "log": {
            "created_at": datetime.now(),
            "creator_user_id": setup_db['user_1'],
            "updated_at": datetime.now(),
            "updater_user_id": setup_db['user_2']
        }
    }
    schema = BulletinsMasterRead(**data)
    assert schema.id == data["id"]
    assert schema.bulletin_name == "Test Bulletin"
    assert schema.current_version_id == data["current_version_id"]
    assert schema.access_config.access_type.value == "public"

def test_read_invalid_schema(setup_db):
    data = {
        "bulletin_name": "Test Bulletin",
        "status": "draft",
        "base_template_master_id": setup_db['template_master'],
        "base_template_version_id": setup_db['template_version'],
        "current_version": setup_db['bulletin_version'],
        "access_config": {
            "access_type": "public",
            "allowed_groups": []
        },
        "log": {
            "created_at": datetime.now(),
            "creator_user_id": setup_db['user_1'],
            "updated_at": datetime.now(),
            "updater_user_id": setup_db['user_2']
        }
    }
    with pytest.raises(ValidationError):
        BulletinsMasterRead(**data)
