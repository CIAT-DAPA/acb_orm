from mongoengine import EmbeddedDocument, StringField

class TargetElement(EmbeddedDocument):
    """
    Embedded document to link a comment to a specific part of a bulletin.
    """
    section_id = StringField()
    block_id = StringField()
    field_id = StringField()
