# Importaciones de la biblioteca estándar
import pytest
from datetime import datetime
from bson import ObjectId
from acb_orm.collections.templates_version import TemplatesVersion
from acb_orm.collections.templates_master import TemplatesMaster
from acb_orm.collections.bulletins_master import BulletinsMaster
from acb_orm.collections.bulletins_version import BulletinsVersion
from acb_orm.collections.users import User
from acb_orm.collections.roles import Role
from acb_orm.auxiliaries.log import Log
from acb_orm.auxiliaries.access_config import AccessConfig

# Importaciones de MongoEngine y mongomock
from mongoengine import Document, StringField, connect, disconnect
import mongomock

# --- FIXTURES DE PYTEST ---

@pytest.fixture(scope="session")
def db_connection():
    """
    Conecta y desconecta de la base de datos de mongomock.
    Se ejecuta una sola vez por sesión de prueba.
    """
    connect("test_db", host="localhost", mongo_client_class=mongomock.MongoClient)
    yield
    disconnect()

@pytest.fixture(scope="function")
def setup_db(db_connection):
    """
    Crea los documentos de prueba necesarios para las validaciones de Pydantic
    antes de cada prueba. Al usar yield, se asegura que los datos se limpien
    después de cada prueba para mantenerlas aisladas.
    """
    # Ids de ejemplo que tus tests necesitan para la validación
    user_id_1 = ObjectId('650d5a32c74d081f9b36d654')
    user_id_2 = ObjectId('650d5a32c74d081f9b36d655')
    user_id_3 = ObjectId('650d5a32c74d081f9b36d656')
    user_id_4 = ObjectId('650d5a32c74d081f9b36d657')
    template_version_id = ObjectId('650d5a32c74d081f9b36d658')
    template_master_id = ObjectId('650d5a32c74d081f9b36d659')
    bulletin_master_id = ObjectId('650d5a32c74d081f9b36d660')
    bulletin_version_id = ObjectId('650d5a32c74d081f9b36d661')
    role_id_admin = ObjectId('650d5a32c74d081f9b36d662')
    role_id_editor = ObjectId('650d5a32c74d081f9b36d663')
    
    # Crear los documentos con los IDs específicos
    User(id=user_id_1, ext_id='Test User 1').save()
    User(id=user_id_2, ext_id='Test User 2').save()
    User(id=user_id_3, ext_id='Test User 3').save()
    User(id=user_id_4, ext_id='Test User 4').save()
    valid_log = {
        'created_at': datetime.now(),
        'creator_user_id': str(user_id_1),
    }
    
    TemplatesVersion(id=template_version_id,
        version_num="1.0",
        log=Log(**valid_log),
        commit_message="Initial commit",
        content={"key": "value"}).save()
    
    TemplatesMaster(id=template_master_id,
        template_name="Master Template",
        status="active",
        log=Log(**valid_log)).save()

    # Ejemplo de AccessConfig mínimo (ajusta según tu modelo)
    access_config = {
        'access_type': "public",
        'allowed_groups': []
    }

    # Crear BulletinMaster de ejemplo
    BulletinsMaster(
        id=bulletin_master_id,
        bulletin_name="Ejemplo Bulletin",
        base_template_master_id=template_master_id,
        base_template_version_id=template_version_id,
        current_version_id=None,
        status="draft",
        access_config=AccessConfig(**access_config),
        log=Log(**valid_log)
    ).save()

    # Crear BulletinVersion de ejemplo
    BulletinsVersion(
        id=bulletin_version_id,
        bulletin_master_id=bulletin_master_id,
        version_num="1.0",
        previous_version_id=None,
        log=Log(**valid_log),
        data={"campo": "valor"}
    ).save()

    # Crear roles de ejemplo
    Role(id=role_id_admin,
         role_name="admin",
         description="Administrador del sistema",
         permissions={"manage_users": True, "edit_content": True},
         log=Log(**valid_log)
    ).save()
    Role(id=role_id_editor,
         role_name="editor",
         description="Editor de contenido",
         permissions={"edit_content": True},
         log=Log(**valid_log)
    ).save()

    yield {
        'user_1': str(user_id_1),
        'user_2': str(user_id_2),
        'user_3': str(user_id_3),
        'user_4': str(user_id_4),
        'template_version': str(template_version_id),
        'template_master': str(template_master_id),
        'bulletin_master': str(bulletin_master_id),
        'bulletin_version': str(bulletin_version_id),
        'role_admin': str(role_id_admin),
        'role_editor': str(role_id_editor)
    }

    # Limpiar las colecciones después del test
    User.objects.delete()
    TemplatesVersion.objects.delete()
    TemplatesMaster.objects.delete()
    BulletinsMaster.objects.delete()
    BulletinsVersion.objects.delete()
    Role.objects.delete()
