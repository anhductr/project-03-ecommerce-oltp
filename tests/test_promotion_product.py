from datetime import datetime

import pytest

from ecommerce.generators.brand import generate_brands
from ecommerce.generators.category import generate_categories
from ecommerce.generators.product import generate_products
from ecommerce.generators.promotion import generate_promotions
from ecommerce.generators.promotion_product import generate_promotion_products
from ecommerce.generators.seller import generate_sellers
from ecommerce.utils.faker_utils import seed_generators

PROJECT_AS_OF = datetime(2025, 5, 31, 23, 59, 59)


def generate_reference_data():
    seed_generators(42)

    brands = generate_brands()
    categories = generate_categories()
    sellers = generate_sellers()

    products = generate_products(
        brands,
        categories,
        sellers,
    )

    promotions = generate_promotions()

    return promotions, products


def test_generate_500_promotion_products():
    promotions, products = generate_reference_data()

    result = generate_promotion_products(
        promotions,
        products,
    )

    assert len(result) == 500

    assert [
        item["promo_product_id"] for item in result
    ] == list(range(1, 501))


def test_promotion_product_foreign_keys():
    promotions, products = generate_reference_data()

    result = generate_promotion_products(
        promotions,
        products,
        count=100,
    )

    promotion_ids = {
        promotion["promotion_id"]
        for promotion in promotions
        if not promotion["is_deleted"]
    }

    product_ids = {
        product["product_id"]
        for product in products
        if not product["is_deleted"] and product["is_active"]
    }

    for item in result:
        assert item["promotion_id"] in promotion_ids
        assert item["product_id"] in product_ids


def test_promotion_product_unique_pairs():
    promotions, products = generate_reference_data()

    result = generate_promotion_products(
        promotions,
        products,
    )

    pairs = [
        (item["promotion_id"], item["product_id"])
        for item in result
    ]

    assert len(pairs) == len(set(pairs))


def test_promotion_product_created_at():
    promotions, products = generate_reference_data()

    result = generate_promotion_products(
        promotions,
        products,
    )

    promotion_by_id = {
        item["promotion_id"]: item
        for item in promotions
    }

    product_by_id = {
        item["product_id"]: item
        for item in products
    }

    start = datetime(2025, 1, 1)

    for item in result:
        promotion = promotion_by_id[item["promotion_id"]]
        product = product_by_id[item["product_id"]]

        created_start = max(
            start,
            promotion["created_at"],
            product["created_at"],
        )

        assert created_start <= item["created_at"] <= PROJECT_AS_OF


def test_promotion_product_audit_fields():
    promotions, products = generate_reference_data()

    result = generate_promotion_products(
        promotions,
        products,
        count=100,
    )

    audit_columns = {
        "created_at",
        "created_by",
        "updated_at",
        "updated_by",
        "is_deleted",
        "deleted_at",
        "deleted_by",
    }

    for item in result:
        assert audit_columns.issubset(item.keys())

        assert item["created_by"] == "data_generator"

        if item["updated_at"] is not None:
            assert item["updated_at"] >= item["created_at"]

        if item["is_deleted"]:
            assert item["deleted_at"] is not None
            assert item["deleted_by"] is not None

            delete_start = (
                item["updated_at"] or item["created_at"]
            )

            assert item["deleted_at"] >= delete_start
        else:
            assert item["deleted_at"] is None
            assert item["deleted_by"] is None


def test_invalid_promotion_product_count():
    promotions, products = generate_reference_data()

    with pytest.raises(ValueError):
        generate_promotion_products(
            promotions,
            products,
            count=0,
        )


def test_empty_reference_data():
    promotions, products = generate_reference_data()

    with pytest.raises(ValueError):
        generate_promotion_products([], products)

    with pytest.raises(ValueError):
        generate_promotion_products(promotions, [])


def test_insufficient_combinations():
    promotions = [
        {
            "promotion_id": 1,
            "is_deleted": False,
            "created_at": datetime(2025, 1, 1),
        }
    ]

    products = [
        {
            "product_id": 1,
            "is_deleted": False,
            "is_active": True,
            "created_at": datetime(2024, 6, 1),
        }
    ]

    with pytest.raises(ValueError):
        generate_promotion_products(
            promotions,
            products,
            count=2,
        )