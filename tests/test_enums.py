import pytest
from acb_orm.enums import get_all_enums, get_enum, get_enum_names

def test_get_all_enums_returns_dict():
    enums = get_all_enums()
    assert isinstance(enums, dict)
    # Debe contener al menos AccessType si existe en el paquete
    assert "AccessType" in enums
    assert isinstance(enums["AccessType"], list)
    assert "public" in enums["AccessType"] or "PUBLIC" in enums["AccessType"]

def test_get_enum_existing_and_non_existing():
    access = get_enum("AccessType")
    assert isinstance(access, list)
    assert any(v in ("public", "PUBLIC", "restricted", "RESTRICTED") for v in access)
    assert get_enum("ThisEnumDoesNotExist") is None

def test_get_enum_names_returns_list():
    names = get_enum_names()
    assert isinstance(names, list)
    assert "AccessType" in names
    assert all(isinstance(name, str) for name in names)
