from datetime import date, datetime
from decimal import Decimal

import pytest

from ecommerce.generators.promotion import generate_promotions
from ecommerce.utils.faker_utils import seed_generators


def test_generate_30_promotions():
    seed_generators(42)

    promotions = generate_promotions()

    assert len(promotions) == 30

    assert [promotion["promotion_id"] for promotion in promotions] == list(
        range(1, 31)
    )


def test_promotion_types():
    seed_generators(42)

    promotions = generate_promotions()

    valid_types = {
        "product",
        "category",
        "seller",
        "flash_sale",
    }

    for promotion in promotions:
        assert promotion["promotion_type"] in valid_types


def test_discount_business_rules():
    seed_generators(42)

    promotions = generate_promotions()

    for promotion in promotions:

        assert promotion["discount_type"] in {
            "percentage",
            "fixed_amount",
        }

        assert isinstance(promotion["discount_value"], Decimal)

        assert promotion["discount_value"] > 0

        if promotion["discount_type"] == "percentage":
            assert promotion["discount_value"] <= 100


def test_promotion_date_rules():
    seed_generators(42)

    promotions = generate_promotions()

    start_min = date(2025, 1, 1)
    start_max = date(2025, 4, 30)

    for promotion in promotions:

        start_date = promotion["start_date"]
        end_date = promotion["end_date"]
        created_at = promotion["created_at"]

        assert start_min <= start_date <= start_max

        assert end_date >= start_date

        duration = (end_date - start_date).days

        assert 30 <= duration <= 50

        assert created_at.date() <= start_date

        assert created_at >= datetime(2024, 12, 1)


def test_promotion_audit_fields():
    seed_generators(42)

    promotions = generate_promotions()

    audit_columns = {
        "created_at",
        "created_by",
        "updated_at",
        "updated_by",
        "is_deleted",
        "deleted_at",
        "deleted_by",
    }

    for promotion in promotions:

        assert audit_columns.issubset(promotion.keys())

        assert promotion["created_by"] == "data_generator"

        if promotion["updated_at"] is not None:
            assert promotion["updated_at"] >= promotion["created_at"]

        if promotion["is_deleted"]:
            assert promotion["deleted_at"] is not None
            assert promotion["deleted_by"] is not None

            delete_start = (
                promotion["updated_at"] or promotion["created_at"]
            )

            assert promotion["deleted_at"] >= delete_start

        else:
            assert promotion["deleted_at"] is None
            assert promotion["deleted_by"] is None


def test_invalid_promotion_count():
    with pytest.raises(ValueError):
        generate_promotions(count=0)