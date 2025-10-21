from datetime import datetime
import pytest
from bson import ObjectId
from pydantic import ValidationError

from acb_orm.collections.cards import Cards
from acb_orm.schemas.cards_schema import CardsCreate, CardsUpdate, CardsRead
from acb_orm.auxiliaries.log import Log
from acb_orm.auxiliaries.access_config import AccessConfig
from acb_orm.enums.card_type import CardType

def test_create_cards_model(db_connection, setup_db):
    log_data = {'created_at': datetime.now(), 'creator_user_id': setup_db['user_1']}
    log = Log(**log_data)
    access_config = AccessConfig(access_type='public', allowed_groups=[])
    card = Cards(
        card_name="Card Test",
        card_type=CardType.PEST_OR_DISEASE,  # use enum member
        templates_master_ids=[ObjectId(setup_db['template_master'])],
        access_config=access_config,
        content={"title": "Card Title", "body": "Card Body"},
        log=log
    )
    card.save()
    assert card.id is not None
    # normalize value for assertion
    ct = card.card_type.value if hasattr(card.card_type, 'value') else card.card_type
    assert ct == CardType.PEST_OR_DISEASE.value
    assert "title" in card.content

def test_retrieve_cards_document(db_connection, setup_db):
    log_data = {'created_at': datetime.now(), 'creator_user_id': setup_db['user_1']}
    log = Log(**log_data)
    access_config = AccessConfig(access_type='public', allowed_groups=[])
    card = Cards(
        card_name="Card Retrieve",
        card_type=CardType.CROP_INFO,
        templates_master_ids=[ObjectId(setup_db['template_master'])],
        access_config=access_config,
        content={"title": "Retrieve Title"},
        log=log
    )
    card.save()
    retrieved_card = Cards.objects.get(card_name="Card Retrieve")
    assert retrieved_card is not None
    ct = retrieved_card.card_type.value if hasattr(retrieved_card.card_type, 'value') else retrieved_card.card_type
    assert ct == CardType.CROP_INFO.value
    assert retrieved_card.content["title"] == "Retrieve Title"

# --- PRUEBAS DE ESQUEMAS DE PYDANTIC ---

def test_create_schema_valid(setup_db):
    data = {
        "card_name": "Card Test",
        "card_type": CardType.PEST_OR_DISEASE,  # enum member accepted by pydantic
        "templates_master_ids": [setup_db['template_master']],
        "access_config": {
            "access_type": "public",
            "allowed_groups": []
        },
        "content": {"title": "Card Title", "body": "Card Body"},
        "log": {
            "created_at": datetime.now(),
            "creator_user_id": setup_db['user_1']
        }
    }
    schema = CardsCreate(**data)
    assert schema.card_name == "Card Test"
    # schema.card_type is an enum member
    assert getattr(schema.card_type, "value", schema.card_type) == CardType.PEST_OR_DISEASE.value
    assert schema.content["title"] == "Card Title"

def test_create_schema_invalid(setup_db):
    data = {
        "card_type": CardType.PEST_OR_DISEASE,
        "templates_master_ids": [setup_db['template_master']],
        "access_config": {
            "access_type": "public",
            "allowed_groups": []
        },
        "content": {"title": "Card Title"},
        "log": {
            "created_at": datetime.now(),
            "creator_user_id": setup_db['user_1']
        }
    }
    with pytest.raises(ValidationError):
        CardsCreate(**data)

def test_update_schema_valid(setup_db):
    data = {
        "card_name": "Card Updated",
        "card_type": CardType.CROP_INFO,
        "templates_master_ids": [setup_db['template_master']],
        "access_config": {
            "access_type": "public",
            "allowed_groups": []
        },
        "content": {"title": "Updated Title"},
        "log": {
            "updated_at": datetime.now(),
            "updater_user_id": setup_db['user_2']
        }
    }
    schema = CardsUpdate(**data)
    assert schema.card_name == "Card Updated"
    assert getattr(schema.card_type, "value", schema.card_type) == CardType.CROP_INFO.value
    assert schema.content["title"] == "Updated Title"

def test_read_schema_valid(setup_db):
    data = {
        "id": str(ObjectId()),
        "card_name": "Card Test",
        "card_type": CardType.PEST_OR_DISEASE,
        "templates_master_ids": [setup_db['template_master']],
        "access_config": {
            "access_type": "public",
            "allowed_groups": []
        },
        "content": {"title": "Card Title", "body": "Card Body"},
        "log": {
            "created_at": datetime.now(),
            "creator_user_id": setup_db['user_1']
        }
    }
    schema = CardsRead(**data)
    assert schema.id == data["id"]
    assert schema.card_name == "Card Test"
    assert getattr(schema.card_type, "value", schema.card_type) == CardType.PEST_OR_DISEASE.value
    assert schema.content["title"] == "Card Title"

def test_read_schema_invalid(setup_db):
    data = {
        "card_type": CardType.PEST_OR_DISEASE,
        "templates_master_ids": [setup_db['template_master']],
        "access_config": {
            "access_type": "public",
            "allowed_groups": []
        },
        "content": {"title": "Card Title"},
        "log": {
            "created_at": datetime.now(),
            "creator_user_id": setup_db['user_1']
        }
    }
    with pytest.raises(ValidationError):
        CardsRead(**data)
