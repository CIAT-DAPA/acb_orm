from datetime import datetime
import pytest
from bson import ObjectId
from pydantic import ValidationError

# Importaciones de tu proyecto
from acb_orm.collections.templates_version import TemplatesVersion
from acb_orm.schemas.templates_version_schema import TemplatesVersionCreate, TemplatesVersionRead, TemplatesVersionUpdate
from acb_orm.auxiliaries.log import Log

# --- PRUEBAS DEL MODELO DE MONGOENGINE ---

def test_create_templates_version_model(db_connection, setup_db):
    """
    Prueba la creación de un documento TemplatesVersion de MongoEngine.
    """
    template_master_id = ObjectId(setup_db['template_master'])
    log_data = {'created_at': datetime.now(), 'creator_user_id': str(ObjectId())}
    log = Log(**log_data)
    
    template_version = TemplatesVersion(
        template_master_id=template_master_id,
        version_num="1.0",
        commit_message="Initial version",
        content={"design": "A simple template"},
        log=log
    )
    template_version.save()
    assert template_version.id is not None
    assert template_version.version_num == "1.0"
    
def test_retrieve_templates_version_document(setup_db):
    """
    Prueba que un documento TemplatesVersion se puede recuperar de la base de datos
    correctamente usando su ID.
    """
    template_version_id = setup_db['template_version']
    retrieved_template = TemplatesVersion.objects.get(id=template_version_id)
    
    assert retrieved_template is not None
    assert retrieved_template.version_num == "1.0"
    assert retrieved_template.commit_message == "Initial commit"
    assert "key" in retrieved_template.content


# --- PRUEBAS DE ESQUEMAS DE PYDANTIC ---

def test_create_schema_valid(setup_db):
    """
    Prueba un esquema de creación válido para TemplatesVersion.
    """
    data = {
        "template_master_id": setup_db['template_master'],
        "previous_version_id": None,
        "version_num": "1.1",
        "commit_message": "Added new fields",
        "content": {"title": "New Template", "body": "lorem ipsum"},
        "log": {
            "created_at": datetime.now(),
            "creator_user_id": setup_db['user_1']
        }
    }
    schema = TemplatesVersionCreate(**data)
    assert schema.version_num == "1.1"
    assert schema.template_master_id == data["template_master_id"]
    assert schema.commit_message == "Added new fields"
    

def test_create_schema_invalid_master_reference(setup_db):
    """
    Prueba que la creación falla si el template_master_id no existe.
    """
    non_existent_master_id = str(ObjectId())
    data = {
        "template_master_id": non_existent_master_id,
        "version_num": "1.1",
        "commit_message": "Added new fields",
        "content": {"title": "New Template"},
        "log": {
            "created_at": datetime.now(),
            "creator_user_id": setup_db['user_1']
        }
    }
    with pytest.raises(ValidationError):
        TemplatesVersionCreate(**data)


def test_update_schema_valid(setup_db):
    """
    Prueba un esquema de actualización válido.
    """
    data = {
        "commit_message": "Updated message",
        "log": {
            "updated_at": datetime.now(),
            "updater_user_id": setup_db['user_2']
        }
    }
    schema = TemplatesVersionUpdate(**data)
    assert schema.commit_message == "Updated message"
    assert schema.log.updater_user_id == setup_db['user_2']


def test_update_schema_invalid_previous_version_reference(setup_db):
    """
    Prueba que la actualización falla si el previous_version_id no existe.
    """
    non_existent_version_id = str(ObjectId())
    data = {
        "commit_message": "Updated message",
        "previous_version_id": non_existent_version_id,
        "log": {
            "updated_at": datetime.now(),
            "updater_user_id": setup_db['user_2']
        }
    }
    with pytest.raises(ValidationError):
        TemplatesVersionUpdate(**data)


def test_read_schema_valid(setup_db):
    """
    Prueba el esquema de lectura válido.
    """
    data = {
        "id": setup_db['template_version'],
        "template_master_id": setup_db['template_master'],
        "previous_version_id": None,
        "version_num": "1.0",
        "commit_message": "Initial commit",
        "content": {"key": "value"},
        "log": {
            "created_at": datetime.now(),
            "creator_user_id": setup_db['user_1']
        }
    }
    schema = TemplatesVersionRead(**data)
    assert schema.id == data['id']
    assert schema.version_num == "1.0"
    assert schema.content == {"key": "value"}