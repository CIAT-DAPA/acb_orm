from datetime import datetime
import pytest
from bson import ObjectId
from mongoengine import connect, disconnect
from pydantic import ValidationError
from acb_orm.collections.templates_master import TemplatesMaster
from acb_orm.schemas.templates_master_schema import TemplatesMasterCreate, TemplatesMasterRead, TemplatesMasterUpdate
from acb_orm.auxiliaries.log import Log
from acb_orm.auxiliaries.access_config import AccessConfig
from acb_orm.enums.status_template import StatusTemplate
from acb_orm.enums.access_type import AccessType

@pytest.fixture
def non_existent_version_id():
    return str(ObjectId())

@pytest.fixture
def non_existent_user_id():
    return str(ObjectId())

# --- PRUEBAS ---

def test_create_templates_master_model(db_connection):
    """
    Prueba la creación de un documento TemplatesMaster de MongoEngine.
    """
    log_data = {'created_at': datetime.now(), 'creator_user_id': str(ObjectId())}
    log = Log(**log_data)
    access_config = AccessConfig(access_type='public', allowed_groups=[])
    template = TemplatesMaster(
        template_name="Test Template",
        description="A test template",
        status=StatusTemplate.ACTIVE,
        access_config=access_config,
        log=log
    )
    template.save()

def test_retrieve_templates_master_document(setup_db):
    """
    Prueba que un documento TemplatesMaster se puede recuperar de la base de datos
    correctamente usando su ID.
    """
    template_master_id = setup_db['template_master']
    retrieved_template = TemplatesMaster.objects.get(id=template_master_id)
    assert retrieved_template is not None
    assert retrieved_template.template_name == "Master Template"

def test_create_schema_valid(setup_db):
    """
    Prueba el esquema de Pydantic para la creación de plantillas, usando datos
    previamente creados por el fixture setup_db de conftest.py.
    """
    data = {
        "template_name": "Test Template",
        "description": "A test template",
        "status": "active",
        "access_config": {
            "access_type": "public",
            "allowed_groups": []
        },
        "log": {
            "created_at": datetime.now(),
            "creator_user_id": setup_db['user_1']
        }
    }
    schema = TemplatesMasterCreate(**data)
    assert schema.template_name == "Test Template"
    assert schema.status == StatusTemplate.ACTIVE
    assert schema.access_config.access_type.value == "public"

def test_create_schema_invalid_reference(non_existent_version_id, non_existent_user_id):
    """
    Prueba el esquema de creación con un ID de referencia inválido (no existe).
    """
    data = {
        "template_name": "Test Template",
        "description": "A test template",
        "status": "active",
        "current_version_id": non_existent_version_id,
        "access_config": {'access_type': 'public', 'allowed_groups': []},
        "log": {
            "created_at": datetime.now(),
            "creator_user_id": non_existent_user_id
        }
    }
    with pytest.raises(ValidationError):
        TemplatesMasterCreate(**data)

def test_update_schema_valid(setup_db):
    """
    Prueba un esquema de actualización válido.
    """
    data = {
        "template_name": "Updated Template",
        "description": "Updated description",
        "status": "archived",
        "current_version_id": setup_db['template_version'],
        "access_config": None,
        "log": {
            "updated_at": datetime.now(),
            "updater_user_id": setup_db['user_2']
        }
    }
    schema = TemplatesMasterUpdate(**data)
    assert schema.template_name == "Updated Template"

def test_update_schema_invalid_reference(non_existent_version_id, non_existent_user_id):
    """
    Prueba el esquema de actualización con un ID de referencia inválido (no existe).
    """
    data = {
        "template_name": "Updated Template",
        "description": "Updated description",
        "status": "archived",
        "current_version_id": non_existent_version_id,
        "access_config": None,
        "log": {
            "updated_at": datetime.now(),
            "updater_user_id": non_existent_user_id
        }
    }
    with pytest.raises(ValidationError):
        TemplatesMasterUpdate(**data)

def test_read_schema():
    """
    Prueba el esquema de lectura.
    """
    data = {
        "id": str(ObjectId()),
        "template_name": "Test Template",
        "description": "A test template",
        "status": "active",
        "current_version_id": str(ObjectId()),
        "access_config": {
            "access_type": "public",
            "allowed_groups": []
        },
        "log": {
            "created_at": datetime.now(),
            "creator_user_id": str(ObjectId()),
            "updated_at": datetime.now(),
            "updater_user_id": str(ObjectId())
        }
    }
    schema = TemplatesMasterRead(**data)
    assert schema.id == data["id"]
    assert schema.template_name == "Test Template"
    assert schema.current_version_id == data["current_version_id"]
    assert schema.access_config.access_type == AccessType.PUBLIC


def test_read_invalid_schema():
    """
    Prueba el esquema de lectura con erros.
    """
    data = {
        "template_name": "Test Template",
        "description": "A test template",
        "status": "active",
        "current_version": str(ObjectId()),
        "access_config": {
            "access_type": "public",
            "allowed_groups": []
        },
        "log": {
            "created_at": datetime.now(),
            "creator_user_id": str(ObjectId()),
            "updated_at": datetime.now(),
            "updater_user_id": str(ObjectId())
        }
    }
    
    with pytest.raises(ValidationError):
        TemplatesMasterRead(**data)
