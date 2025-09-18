# Bulletin Builder ORM 💡📄

## 📌 Introducción

Bulletin Builder ORM es una capa de abstracción basada en Python y MongoEngine para interactuar con una base de datos MongoDB. Este ORM facilita la gestión de datos para la aplicación Bulletin Builder, proporcionando una interfaz robusta y mantenible para operaciones CRUD y control de acceso.


## 🏷️ Versión & Etiquetas

![GitHub release (latest by date)](https://img.shields.io/github/v/release/CIAT-DAPA/acb_orm)
![GitHub tag (latest by date)](https://img.shields.io/github/v/tag/CIAT-DAPA/acb_orm)

## 📖 Documentación

Consulta la documentación completa en [![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/CIAT-DAPA/acb_orm)

## ✨ Features

- Estructura modular por dominio (templates, bulletins, cards, users, roles, groups, reviews, visual resources)
- Basado en MongoEngine para mapeo eficiente con MongoDB
- Compatible con Python > 3.10
- Esquemas Pydantic para validación robusta y serialización
- Fácil integración en sistemas Bulletin Builder y otros proyectos

## ✅ Requerimientos

- Python > 3.10
- MongoDB (local o remoto)
- Dependencias:
  - mongoengine
  - pymongo
  - dnspython
  - python-dotenv
  - pydantic
  - typing_extensions

## 🚀 Instalación

Instala directamente desde GitHub:

```bash
pip install git+https://github.com/CIAT-DAPA/acb_orm
```

Para instalar una versión específica:

```bash
pip install git+https://github.com/CIAT-DAPA/acb_orm@v0.0.1
```

## 🔧 Configuración de entorno

Configura la conexión a la base de datos creando un archivo `.env` en la raíz del proyecto o estableciendo variables de entorno:

```ini
DATABASE_URI=mongodb://usuario:contraseña@localhost:27017
DATABASE_NAME=bulletin_builder
```

## 🏗️ Estructura del Proyecto

```bash
acb_orm/
│
├── src/
│   └── acb_orm/
│       ├── collections/      # Modelos MongoEngine para cada colección
│       ├── schemas/          # Esquemas Pydantic para validación
│       ├── auxiliaries/      # Documentos embebidos y utilidades
│       ├── enums/            # Enumeraciones para estados y tipos
│       ├── validations/      # Validaciones personalizadas
│
├── tests/                    # Pruebas unitarias y de integración
├── pyproject.toml            # Configuración del paquete
└── README.md                 # Documentación principal
```

## 🧪 Pruebas

Ejecuta todos los tests con:

```bash
PYTHONPATH=src pytest tests/
```

## 🗂️ Colecciones de la Base de Datos

La base de datos está organizada en las siguientes colecciones, cada una con su propósito y estructura específica:

### templates_master

Repositorio principal de plantillas, agrupando todas sus versiones y metadatos.

- `_id`: ObjectId
- `template_name`: string
- `description`: string
- `log`: objeto de auditoría (created_at, creator_user_id, updated_at, updater_user_id)
- `status`: string (ej. "activa", "archivada")
- `current_version_id`: referencia a `templates_versions`
- `access_config`: objeto de control de acceso (`access_type`, `allowed_groups`)

### templates_versions

Almacena cada versión individual de una plantilla como snapshot inmutable.

- `_id`: ObjectId
- `template_master_id`: referencia a `templates_master`
- `version_num`: string o número
- `previous_version_id`: referencia a versión anterior o null
- `log`: objeto de auditoría
- `commit_message`: string
- `content`: estructura y diseño de la plantilla

### bulletins_master

Índice de boletines, contiene metadatos y referencia a la versión más reciente.

- `_id`: ObjectId
- `bulletin_name`: string
- `base_template_master_id`: referencia a `templates_master`
- `base_template_version_id`: referencia a `templates_versions`
- `current_version_id`: referencia a `bulletins_versions`
- `status`: string (ej. "draft", "published")
- `log`: objeto de auditoría

### bulletins_versions

Almacena cada versión completa e inmutable de un boletín.

- `_id`: ObjectId
- `bulletin_master_id`: referencia a `bulletins_master`
- `version_num`: número o string
- `previous_version_id`: referencia a versión anterior o null
- `log`: objeto de auditoría
- `data`: estructura completa del boletín con campos llenos

### bulletin_reviews

Registro de cada ciclo de revisión de un boletín.

- `_id`: ObjectId
- `bulletin_master_id`: referencia a `bulletins_master`
- `reviewer_user_id`: referencia a `users`
- `log`: objeto de auditoría
- `completed_at`: fecha de finalización
- `comments`: array de comentarios y respuestas anidadas

### visual_resources

Catálogo de metadatos para archivos visuales.

- `_id`: ObjectId
- `file_url`: string
- `file_name`: string
- `file_type`: string
- `tags`: array de strings
- `log`: objeto de auditoría

### cards

Biblioteca de contenido reutilizable para boletines.

- `_id`: ObjectId
- `card_name`: string
- `card_type`: string
- `templates_master_ids`: array de referencias a `templates_master`
- `access_config`: objeto de control de acceso
- `content`: estructura flexible de la card

### users

Información de usuarios y control de acceso.

- `_id`: ObjectId
- `ext_id`: string (ID externo, ej. keycloak)
- `is_active`: boolean
- `log`: objeto de auditoría

### roles

Define los roles y permisos de la plataforma.

- `_id`: ObjectId
- `role_name`: string
- `description`: string
- `permissions`: objeto CRUD por módulo
- `log`: objeto de auditoría

### groups

Organiza usuarios por afiliación y país.

- `_id`: ObjectId
- `group_name`: string
- `country`: string
- `description`: string
- `users_access`: array de objetos `{user_id, role_id}`
- `log`: objeto de auditoría


