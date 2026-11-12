from datetime import datetime

import pytest

from ecommerce.utils.audit_utils import generate_audit_fields
from ecommerce.utils.faker_utils import seed_generators

CREATED_AT = datetime(2024, 5, 10, 8, 30, 15)
AS_OF = datetime(2025, 5, 31, 23, 59, 59)


def test_generate_new_record_audit():
    seed_generators(42)

    audit = generate_audit_fields(
        created_at=CREATED_AT,
        as_of=AS_OF,
        update_probability=0,
        delete_probability=0,
    )

    assert audit["created_at"] == CREATED_AT
    assert audit["created_by"] == "data_generator"
    assert audit["updated_at"] is None
    assert audit["updated_by"] is None
    assert audit["is_deleted"] is False
    assert audit["deleted_at"] is None
    assert audit["deleted_by"] is None


def test_generate_updated_record_audit():
    seed_generators(42)

    audit = generate_audit_fields(
        created_at=CREATED_AT,
        as_of=AS_OF,
        update_probability=1,
        delete_probability=0,
    )

    assert audit["updated_at"] is not None
    assert audit["updated_by"] is not None
    assert CREATED_AT <= audit["updated_at"] <= AS_OF
    assert audit["is_deleted"] is False


def test_generate_deleted_record_audit():
    seed_generators(42)

    audit = generate_audit_fields(
        created_at=CREATED_AT,
        as_of=AS_OF,
        update_probability=1,
        delete_probability=1,
    )

    assert audit["is_deleted"] is True
    assert audit["deleted_at"] is not None
    assert audit["deleted_by"] is not None

    assert audit["deleted_at"] >= audit["updated_at"]
    assert audit["deleted_at"] <= AS_OF


def test_invalid_created_at():
    with pytest.raises(ValueError):
        generate_audit_fields(
            created_at=AS_OF,
            as_of=CREATED_AT,
        )