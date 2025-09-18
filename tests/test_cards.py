from datetime import datetime
import pytest
from bson import ObjectId
from pydantic import ValidationError

from acb_orm.collections.cards import Cards
from acb_orm.schemas.cards_schema import CardsCreate, CardsUpdate, CardsRead
from acb_orm.auxiliaries.log import Log
from acb_orm.auxiliaries.access_config import AccessConfig

def test_create_cards_model(db_connection, setup_db):
    log_data = {'created_at': datetime.now(), 'creator_user_id': setup_db['user_1']}
    log = Log(**log_data)
    access_config = AccessConfig(access_type='public', allowed_groups=[])
    card = Cards(
        card_name="Card Test",
        card_type="pest_or_disease",
        templates_master_ids=[ObjectId(setup_db['template_master'])],
        access_config=access_config,
        content={"title": "Card Title", "body": "Card Body"},
        log=log
    )
    card.save()
    assert card.id is not None
    assert card.card_name == "Card Test"
    assert card.card_type == "pest_or_disease"
    assert "title" in card.content

def test_retrieve_cards_document(db_connection, setup_db):
    log_data = {'created_at': datetime.now(), 'creator_user_id': setup_db['user_1']}
    log = Log(**log_data)
    access_config = AccessConfig(access_type='public', allowed_groups=[])
    card = Cards(
        card_name="Card Retrieve",
        card_type="info",
        templates_master_ids=[ObjectId(setup_db['template_master'])],
        access_config=access_config,
        content={"title": "Retrieve Title"},
        log=log
    )
    card.save()
    retrieved_card = Cards.objects.get(card_name="Card Retrieve")
    assert retrieved_card is not None
    assert retrieved_card.card_type == "info"
    assert retrieved_card.content["title"] == "Retrieve Title"

def test_create_schema_valid(setup_db):
    data = {
        "card_name": "Card Test",
        "card_type": "pest_or_disease",
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
    assert schema.card_type == "pest_or_disease"
    assert schema.content["title"] == "Card Title"

def test_create_schema_invalid(setup_db):
    data = {
        "card_type": "pest_or_disease",
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
        "card_type": "info",
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
    assert schema.card_type == "info"
    assert schema.content["title"] == "Updated Title"

def test_read_schema_valid(setup_db):
    data = {
        "id": str(ObjectId()),
        "card_name": "Card Test",
        "card_type": "pest_or_disease",
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
    assert schema.card_type == "pest_or_disease"
    assert schema.content["title"] == "Card Title"

def test_read_schema_invalid(setup_db):
    data = {
        "card_type": "pest_or_disease",
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
