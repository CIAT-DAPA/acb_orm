import os
from mongoengine import connect

def init_db():
    """
    Initialize the MongoDB connection using environment variables.

    Required environment variables:
    - DATABASE_URI: The full MongoDB connection string.
    - DATABASE_NAME: The name of the database to connect to.
    """
    uri = os.getenv("DATABASE_URI")
    db_name = os.getenv("DATABASE_NAME")
    if not uri or not db_name:
        raise EnvironmentError("DATABASE_URI and DATABASE_NAME must be set as environment variables.")
    connect(db=db_name, host=uri)