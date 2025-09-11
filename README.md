# Bulletin Builder Backend ORM

## Overview

Bulletin Builder Backend ORM is a Python-based abstraction layer utilizing MongoEngine to interact with a MongoDB database. This ORM streamlines database management for the Bulletin Builder application, providing a robust and maintainable interface for data operations.

## Technology Stack

- Python
- MongoEngine
- MongoDB

## Database Structure

The database schema is organized into the following collections, each serving a specific purpose within the Bulletin Builder ecosystem:

- `templates_master`: Main repository for templates, storing high-level metadata and grouping all template versions.
- `templates_versions`: Stores immutable snapshots of each template version, enabling version tracking and rollback.
- `bulletins_master`: Indexes bulletins, holding metadata and references to the latest version.
- `bulletins_versions`: Contains complete, immutable versions of bulletins, allowing historical reconstruction.
- `bulletin_reviews`: Records review cycles for bulletins, including outcomes, comments, and timestamps.
- `visual_resources`: Catalog of metadata for visual files stored on the server, facilitating resource management and search.
- `cards`: Library of reusable content blocks that can be inserted into bulletins.
- `users`: Stores user information, roles, and permissions for system access control.
- `roles`: Defines platform roles and their associated permissions using a CRUD model.
- `groups`: Organizes users by affiliation, typically by geography, and manages group-based access.

