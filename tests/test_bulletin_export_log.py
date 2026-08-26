from datetime import datetime
import pytest
from bson import ObjectId
from pydantic import ValidationError
from mongoengine import ValidationError as MongoValidationError

from acb_orm.collections.bulletin_export_log import BulletinExportLog
from acb_orm.schemas.bulletin_export_log_schema import (
    BulletinExportLogCreate,
    BulletinExportLogUpdate,
    BulletinExportLogRead,
)
from acb_orm.enums.export_format import ExportFormat

@pytest.fixture
def non_existent_id():
    return str(ObjectId())

@pytest.fixture(autouse=True)
def clean_export_logs(db_connection):
    """
    Limpia la coleccion de export logs despues de cada prueba para que los
    documentos creados no se filtren a las demas pruebas.
    """
    yield
    BulletinExportLog.objects.delete()

# --- PRUEBAS DEL MODELO DE MONGOENGINE ---

def test_create_bulletin_export_log_model(db_connection, setup_db):
    export_log = BulletinExportLog(
        user_id=ObjectId(setup_db['user_1']),
        bulletin_master_id=ObjectId(setup_db['bulletin_master']),
        bulletin_version_id=ObjectId(setup_db['bulletin_version']),
        bulletin_title="Ejemplo Bulletin",
        format=ExportFormat.PDF
    )
    export_log.save()
    assert export_log.id is not None
    assert export_log.format == ExportFormat.PDF
    # exported_at se llena por defecto en el modelo
    assert export_log.exported_at is not None

def test_retrieve_bulletin_export_log_document(db_connection, setup_db):
    export_log = BulletinExportLog(
        user_id=ObjectId(setup_db['user_2']),
        bulletin_master_id=ObjectId(setup_db['bulletin_master']),
        bulletin_version_id=ObjectId(setup_db['bulletin_version']),
        bulletin_title="Ejemplo Bulletin",
        format=ExportFormat.HTML,
        exported_at=datetime.now()
    )
    export_log.save()
    retrieved_log = BulletinExportLog.objects.get(id=export_log.id)
    assert retrieved_log is not None
    assert retrieved_log.user_id.id == ObjectId(setup_db['user_2'])
    assert retrieved_log.bulletin_master_id.id == ObjectId(setup_db['bulletin_master'])
    assert retrieved_log.bulletin_version_id.id == ObjectId(setup_db['bulletin_version'])
    assert retrieved_log.format == ExportFormat.HTML

def test_create_bulletin_export_log_model_missing_required(db_connection, setup_db):
    # format es obligatorio en el modelo
    export_log = BulletinExportLog(
        user_id=ObjectId(setup_db['user_1']),
        bulletin_master_id=ObjectId(setup_db['bulletin_master']),
        bulletin_version_id=ObjectId(setup_db['bulletin_version']),
        bulletin_title="Ejemplo Bulletin"
    )
    with pytest.raises(MongoValidationError):
        export_log.save()

# --- PRUEBAS DE ESQUEMAS DE PYDANTIC ---

def test_create_schema_valid(setup_db):
    exported_at = datetime.now()
    data = {
        "user_id": setup_db['user_1'],
        "bulletin_master_id": setup_db['bulletin_master'],
        "bulletin_version_id": setup_db['bulletin_version'],
        "bulletin_title": "Ejemplo Bulletin",
        "format": "pdf",
        "exported_at": exported_at
    }
    schema = BulletinExportLogCreate(**data)
    assert schema.user_id == setup_db['user_1']
    assert schema.bulletin_master_id == setup_db['bulletin_master']
    assert schema.bulletin_version_id == setup_db['bulletin_version']
    assert schema.format == ExportFormat.PDF
    assert schema.exported_at == exported_at

def test_create_schema_defaults_exported_at(setup_db):
    data = {
        "user_id": setup_db['user_1'],
        "bulletin_master_id": setup_db['bulletin_master'],
        "bulletin_version_id": setup_db['bulletin_version'],
        "format": "json"
    }
    schema = BulletinExportLogCreate(**data)
    # exported_at se genera automaticamente y bulletin_title es opcional
    assert schema.exported_at is not None
    assert schema.bulletin_title is None

def test_create_schema_invalid_user_reference(non_existent_id, setup_db):
    data = {
        "user_id": non_existent_id,
        "bulletin_master_id": setup_db['bulletin_master'],
        "bulletin_version_id": setup_db['bulletin_version'],
        "format": "pdf"
    }
    with pytest.raises(ValidationError):
        BulletinExportLogCreate(**data)

def test_create_schema_invalid_bulletin_master_reference(non_existent_id, setup_db):
    data = {
        "user_id": setup_db['user_1'],
        "bulletin_master_id": non_existent_id,
        "bulletin_version_id": setup_db['bulletin_version'],
        "format": "pdf"
    }
    with pytest.raises(ValidationError):
        BulletinExportLogCreate(**data)

def test_create_schema_invalid_bulletin_version_reference(non_existent_id, setup_db):
    data = {
        "user_id": setup_db['user_1'],
        "bulletin_master_id": setup_db['bulletin_master'],
        "bulletin_version_id": non_existent_id,
        "format": "pdf"
    }
    with pytest.raises(ValidationError):
        BulletinExportLogCreate(**data)

def test_create_schema_invalid_object_id_format(setup_db):
    data = {
        "user_id": "no-es-un-object-id",
        "bulletin_master_id": setup_db['bulletin_master'],
        "bulletin_version_id": setup_db['bulletin_version'],
        "format": "pdf"
    }
    with pytest.raises(ValidationError):
        BulletinExportLogCreate(**data)

def test_create_schema_invalid_format(setup_db):
    data = {
        "user_id": setup_db['user_1'],
        "bulletin_master_id": setup_db['bulletin_master'],
        "bulletin_version_id": setup_db['bulletin_version'],
        "format": "docx"
    }
    with pytest.raises(ValidationError):
        BulletinExportLogCreate(**data)

def test_create_schema_missing_required(setup_db):
    # falta user_id
    data = {
        "bulletin_master_id": setup_db['bulletin_master'],
        "bulletin_version_id": setup_db['bulletin_version'],
        "format": "pdf"
    }
    with pytest.raises(ValidationError):
        BulletinExportLogCreate(**data)

def test_update_schema_valid(setup_db):
    schema = BulletinExportLogUpdate(format="jpg", bulletin_title="Titulo corregido")
    assert schema.format == ExportFormat.JPG
    assert schema.bulletin_title == "Titulo corregido"

def test_update_schema_partial(setup_db):
    # todos los campos son opcionales en el update
    schema = BulletinExportLogUpdate()
    assert schema.format is None
    assert schema.bulletin_title is None

def test_update_schema_invalid_format(setup_db):
    with pytest.raises(ValidationError):
        BulletinExportLogUpdate(format="docx")

def test_read_schema_valid(setup_db):
    exported_at = datetime.now()
    data = {
        "id": str(ObjectId()),
        "user_id": setup_db['user_1'],
        "user_first_name": "Test",
        "user_last_name": "User",
        "bulletin_master_id": setup_db['bulletin_master'],
        "bulletin_version_id": setup_db['bulletin_version'],
        "bulletin_title": "Ejemplo Bulletin",
        "format": "pdf",
        "exported_at": exported_at
    }
    schema = BulletinExportLogRead(**data)
    assert schema.id == data["id"]
    assert schema.user_id == setup_db['user_1']
    assert schema.user_first_name == "Test"
    assert schema.format == ExportFormat.PDF
    assert schema.exported_at == exported_at

def test_read_schema_missing_id(setup_db):
    data = {
        "user_id": setup_db['user_1'],
        "bulletin_master_id": setup_db['bulletin_master'],
        "bulletin_version_id": setup_db['bulletin_version'],
        "format": "pdf",
        "exported_at": datetime.now()
    }
    with pytest.raises(ValidationError):
        BulletinExportLogRead(**data)

def test_read_schema_missing_exported_at(setup_db):
    data = {
        "id": str(ObjectId()),
        "user_id": setup_db['user_1'],
        "bulletin_master_id": setup_db['bulletin_master'],
        "bulletin_version_id": setup_db['bulletin_version'],
        "format": "pdf"
    }
    with pytest.raises(ValidationError):
        BulletinExportLogRead(**data)
