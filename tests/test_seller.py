from datetime import date, datetime
from decimal import Decimal

import pytest

from ecommerce.generators.seller import generate_sellers
from ecommerce.utils.faker_utils import seed_generators


def test_generate_50_sellers():
    seed_generators(42)

    sellers = generate_sellers()

    assert len(sellers) == 50

    assert [seller["seller_id"] for seller in sellers] == list(
        range(1, 51)
    )


def test_seller_names_are_unique():
    seed_generators(42)

    sellers = generate_sellers()

    names = [
        seller["seller_name"]
        for seller in sellers
    ]

    assert len(names) == len(set(names))


def test_seller_business_rules():
    seed_generators(42)

    sellers = generate_sellers()

    for seller in sellers:

        assert seller["seller_type"] in {
            "Official",
            "Marketplace",
        }

        assert seller["country"] == "Vietnam"

        assert Decimal("3.0") <= seller["rating"] <= Decimal("5.0")

        assert isinstance(seller["rating"], Decimal)


def test_seller_dates():
    seed_generators(42)

    sellers = generate_sellers()

    start = date(2024, 1, 1)
    end = date(2024, 12, 31)

    for seller in sellers:

        assert start <= seller["join_date"] <= end

        assert seller["created_at"].date() == seller["join_date"]

        assert seller["created_at"] <= datetime(
            2025, 5, 31, 23, 59, 59
        )


def test_seller_audit_fields():
    seed_generators(42)

    sellers = generate_sellers()

    audit_columns = {
        "created_at",
        "created_by",
        "updated_at",
        "updated_by",
        "is_deleted",
        "deleted_at",
        "deleted_by",
    }

    for seller in sellers:

        assert audit_columns.issubset(seller.keys())

        assert seller["created_by"] == "data_generator"

        if seller["is_deleted"]:
            assert seller["deleted_at"] is not None
            assert seller["deleted_by"] is not None
        else:
            assert seller["deleted_at"] is None
            assert seller["deleted_by"] is None


def test_invalid_seller_count():
    with pytest.raises(ValueError):
        generate_sellers(count=0)