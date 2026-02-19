from mongoengine import EmbeddedDocument, ReferenceField, StringField, DateTimeField, IntField, EnumField
from acb_orm.collections.bulletins_version import BulletinsVersion
from acb_orm.enums.outcome_cycle import OutcomeCycle

class ReviewCycle(EmbeddedDocument):
    """Embedded document para rastrear cada ciclo de revisión"""
    cycle_number = IntField(required=True)
    bulletin_version_id = ReferenceField(BulletinsVersion, required=True)
    submitted_at = DateTimeField(required=True)
    completed_at = DateTimeField() 
    outcome = EnumField(OutcomeCycle)