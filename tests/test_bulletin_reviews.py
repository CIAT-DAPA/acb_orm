from datetime import datetime
import pytest
from bson import ObjectId
from pydantic import ValidationError

from acb_orm.collections.bulletin_reviews import BulletinReviews
from acb_orm.schemas.bulletin_reviews_schema import BulletinReviewsCreate, BulletinReviewsUpdate, BulletinReviewsRead
from acb_orm.auxiliaries.log import Log
from acb_orm.auxiliaries.comment import Comment

def test_create_bulletin_reviews_model(db_connection, setup_db):
    log_data = {'created_at': datetime.now(), 'creator_user_id': setup_db['user_1']}
    log = Log(**log_data)
    comment = Comment(
        comment_id="c1",
        bulletin_version_id=ObjectId(setup_db['bulletin_version']),
        text="Comentario de prueba",
        author_id=ObjectId(setup_db['user_1']),
        created_at=datetime.now()
    )
    review = BulletinReviews(
        bulletin_master_id=ObjectId(setup_db['bulletin_master']),
        reviewer_user_id=ObjectId(setup_db['user_2']),
        log=log,
        completed_at=datetime.now(),
        comments=[comment]
    )
    review.save()
    assert review.id is not None
    assert review.bulletin_master_id.id == ObjectId(setup_db['bulletin_master'])
    assert review.reviewer_user_id.id == ObjectId(setup_db['user_2'])
    assert len(review.comments) == 1

def test_retrieve_bulletin_reviews_document(db_connection, setup_db):
    log_data = {'created_at': datetime.now(), 'creator_user_id': setup_db['user_1']}
    log = Log(**log_data)
    comment = Comment(
        comment_id="c2",
        bulletin_version_id=ObjectId(setup_db['bulletin_version']),
        text="Otro comentario",
        author_id=ObjectId(setup_db['user_2']),
        created_at=datetime.now()
    )
    review = BulletinReviews(
        bulletin_master_id=ObjectId(setup_db['bulletin_master']),
        reviewer_user_id=ObjectId(setup_db['user_2']),
        log=log,
        completed_at=datetime.now(),
        comments=[comment]
    )
    review.save()
    retrieved_review = BulletinReviews.objects.get(id=review.id)
    assert retrieved_review is not None
    assert retrieved_review.reviewer_user_id.id == ObjectId(setup_db['user_2'])
    assert len(retrieved_review.comments) == 1

def test_create_schema_valid(setup_db):
    data = {
        "bulletin_master_id": setup_db['bulletin_master'],
        "reviewer_user_id": setup_db['user_2'],
        "log": {
            "created_at": datetime.now(),
            "creator_user_id": setup_db['user_1']
        },
        "completed_at": datetime.now(),
        "comments": [
            {
                "comment_id": "c1",
                "text": "Comentario de prueba",
                "created_at": datetime.now(),
                "bulletin_version_id": setup_db['bulletin_version'],
                "author_id": setup_db['user_1']
            }
        ]
    }
    schema = BulletinReviewsCreate(**data)
    assert schema.bulletin_master_id == setup_db['bulletin_master']
    assert schema.reviewer_user_id == setup_db['user_2']
    assert len(schema.comments) == 1

def test_create_schema_invalid(setup_db):
    data = {
        "reviewer_user_id": setup_db['user_2'],
        "log": {
            "created_at": datetime.now(),
            "creator_user_id": setup_db['user_1']
        },
        "completed_at": datetime.now(),
        "comments": []
    }
    with pytest.raises(ValidationError):
        BulletinReviewsCreate(**data)

def test_update_schema_valid(setup_db):
    data = {
        "completed_at": datetime.now(),
        "log": {
            "updated_at": datetime.now(),
            "updater_user_id": setup_db['user_2']
        },
        "comments": [
            {
                "comment_id": "c2",
                "text": "Comentario actualizado",
                "created_at": datetime.now(),
                "bulletin_version_id": setup_db['bulletin_version'],
                "author_id": setup_db['user_2']
            }
        ]
    }
    schema = BulletinReviewsUpdate(**data)
    assert schema.completed_at is not None
    assert len(schema.comments) == 1

def test_read_schema_valid(setup_db):
    data = {
        "id": str(ObjectId()),
        "bulletin_master_id": setup_db['bulletin_master'],
        "reviewer_user_id": setup_db['user_2'],
        "log": {
            "created_at": datetime.now(),
            "creator_user_id": setup_db['user_1']
        },
        "completed_at": datetime.now(),
        "comments": [
            {
                "comment_id": "c1",
                "text": "Comentario de prueba",
                "created_at": datetime.now(),
                "bulletin_version_id": setup_db['bulletin_version'],
                "author_id": setup_db['user_1'],
                "replies": []
            }
        ]
    }
    schema = BulletinReviewsRead(**data)
    assert schema.id == data["id"]
    assert schema.bulletin_master_id == setup_db['bulletin_master']
    assert schema.reviewer_user_id == setup_db['user_2']
    assert len(schema.comments) == 1

def test_read_schema_invalid(setup_db):
    data = {
        "bulletin_master_id": setup_db['bulletin_master'],
        "reviewer_user_id": setup_db['user_2'],
        "log": {
            "created_at": datetime.now(),
            "creator_user_id": setup_db['user_1']
        },
        "completed_at": datetime.now(),
        "comments": []
    }
    with pytest.raises(ValidationError):
        BulletinReviewsRead(**data)
