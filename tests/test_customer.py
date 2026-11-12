from datetime import datetime

import pytest

from ecommerce.generators.customer import generate_customers
from ecommerce.utils.faker_utils import seed_generators


def test_generate_30000_customers():
    seed_generators(42)

    customers = generate_customers()

    assert len(customers) == 30_000

    assert [customer["customer_id"] for customer in customers] == list(
        range(1, 30_001)
    )


def test_customer_email_and_phone_are_unique():
    seed_generators(42)

    customers = generate_customers(count=1000)

    emails = [customer["email"] for customer in customers]
    phones = [customer["phone"] for customer in customers]

    assert len(emails) == len(set(emails))
    assert len(phones) == len(set(phones))


def test_customer_business_rules():
    seed_generators(42)

    customers = generate_customers(count=100)

    for customer in customers:
        assert customer["gender"] in {"Male", "Female"}

        assert "@" in customer["email"]
        assert len(customer["email"]) <= 150

        assert len(customer["phone"]) == 10
        assert customer["phone"].isdigit()

        assert len(customer["customer_name"]) <= 150
        assert len(customer["address"]) <= 255
        assert len(customer["city"]) <= 100


def test_customer_audit_fields():
    seed_generators(42)

    customers = generate_customers(count=100)

    audit_columns = {
        "created_at",
        "created_by",
        "updated_at",
        "updated_by",
        "is_deleted",
        "deleted_at",
        "deleted_by",
    }

    for customer in customers:
        assert audit_columns.issubset(customer.keys())

        assert customer["created_by"] == "data_generator"

        if customer["updated_at"] is not None:
            assert customer["updated_at"] >= customer["created_at"]

        if customer["is_deleted"]:
            assert customer["deleted_at"] is not None
            assert customer["deleted_by"] is not None

            delete_start = (
                customer["updated_at"] or customer["created_at"]
            )

            assert customer["deleted_at"] >= delete_start
        else:
            assert customer["deleted_at"] is None
            assert customer["deleted_by"] is None


def test_customer_created_at_range():
    seed_generators(42)

    customers = generate_customers(count=100)

    start = datetime(2024, 1, 1)
    end = datetime(2024, 12, 31, 23, 59, 59)

    for customer in customers:
        assert start <= customer["created_at"] <= end


def test_invalid_customer_count():
    with pytest.raises(ValueError):
        generate_customers(count=0)