# Bulletin Builder ORM 💡📄

## 📌 Introduction

Bulletin Builder ORM is a Python and MongoEngine-based abstraction layer for interacting with a MongoDB database. This ORM streamlines data management for the Bulletin Builder application, providing a robust and maintainable interface for CRUD operations and access control.

## 🏷️ Version & Tags

![GitHub release (latest by date)](https://img.shields.io/github/v/release/CIAT-DAPA/acb_orm)
![GitHub tag (latest by date)](https://img.shields.io/github/v/tag/CIAT-DAPA/acb_orm)

## 📖 Documentation

See the complete documentation at [![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/CIAT-DAPA/acb_orm)

## ✨ Features

- Modular structure by domain (templates, bulletins, cards, users, roles, groups, reviews, visual resources)
- Based on MongoEngine for efficient mapping with MongoDB
- Compatible with Python > 3.10
- Pydantic schemas for robust validation and serialization
- Easy integration into Bulletin Builder systems and other projects

## ✅ Requirements

- Python > 3.10
- MongoDB (local or remote)
- Dependencies:
  - mongoengine
  - pymongo
  - dnspython
  - python-dotenv
  - pydantic
  - typing_extensions

## 🚀 Installation

Install directly from GitHub:

```bash
pip install git+https://github.com/CIAT-DAPA/acb_orm
```

To install a specific version:

```bash
pip install git+https://github.com/CIAT-DAPA/acb_orm@v0.0.1
```

## 🔧 Environment Configuration

Configure the database connection by creating a `.env` file in the project root or setting environment variables:

```ini
DATABASE_URI=mongodb://user:password@localhost:27017
DATABASE_NAME=bulletin_builder
```

## 🏗️ Project Structure

```bash
acb_orm/
│
├── src/
│   └── acb_orm/
│       ├── collections/      # MongoEngine models for each collection
│       ├── schemas/          # Pydantic schemas for validation
│       ├── auxiliaries/      # Embedded documents and utilities
│       ├── enums/            # Enumerations for states and types
│       ├── validations/      # Custom validations
│
├── tests/                    # Unit and integration tests
├── pyproject.toml            # Package configuration
└── README.md                 # Main documentation
```

## 🧪 Testing

Run all tests with:

```bash
PYTHONPATH=src pytest tests/
```

## 🗂️ Database Collections

The database is organized into the following collections, each with its specific purpose and structure:

### templates_master

Main template repository, grouping all versions and metadata.

- `_id`: ObjectId
- `template_name`: string
- `description`: string
- `log`: audit object (created_at, creator_user_id, updated_at, updater_user_id)
- `status`: string (e.g., "active", "archived")
- `current_version_id`: reference to `templates_versions`
- `access_config`: access control object (`access_type`, `allowed_groups`)

### templates_versions

Stores each individual version of a template as an immutable snapshot.

- `_id`: ObjectId
- `template_master_id`: reference to `templates_master`
- `version_num`: string or number
- `previous_version_id`: reference to previous version or null
- `log`: audit object
- `commit_message`: string
- `content`: template structure and design

### bulletins_master

Bulletin index, contains metadata and reference to the latest version.

- `_id`: ObjectId
- `bulletin_name`: string
- `base_template_master_id`: reference to `templates_master`
- `base_template_version_id`: reference to `templates_versions`
- `current_version_id`: reference to `bulletins_versions`
- `status`: string (e.g., "draft", "published")
- `log`: audit object

### bulletins_versions

Stores each complete and immutable version of a bulletin.

- `_id`: ObjectId
- `bulletin_master_id`: reference to `bulletins_master`
- `version_num`: number or string
- `previous_version_id`: reference to previous version or null
- `log`: audit object
- `data`: complete bulletin structure with filled fields

### bulletin_reviews

Record of each bulletin review cycle.

- `_id`: ObjectId
- `bulletin_master_id`: reference to `bulletins_master`
- `reviewer_user_id`: reference to `users`
- `log`: audit object
- `completed_at`: completion date
- `comments`: array of comments and nested replies

### visual_resources

Metadata catalog for visual files.

- `_id`: ObjectId
- `file_url`: string
- `file_name`: string
- `file_type`: string
- `tags`: array of strings
- `log`: audit object

### cards

Reusable content library for bulletins.

- `_id`: ObjectId
- `card_name`: string
- `card_type`: string
- `templates_master_ids`: array of references to `templates_master`
- `access_config`: access control object
- `content`: flexible card structure

### users

User information and access control.

- `_id`: ObjectId
- `ext_id`: string (external ID, e.g., keycloak)
- `is_active`: boolean
- `log`: audit object

### roles

Defines platform roles and permissions.

- `_id`: ObjectId
- `role_name`: string
- `description`: string
- `permissions`: CRUD object per module
- `log`: audit object

### groups

Organizes users by affiliation and country.

- `_id`: ObjectId
- `group_name`: string
- `country`: string
- `description`: string
- `users_access`: array of objects `{user_id, role_id}`
- `log`: audit object
