from datetime import datetime
from decimal import Decimal

import pytest

from ecommerce.generators.brand import generate_brands
from ecommerce.generators.category import generate_categories
from ecommerce.generators.product import generate_products
from ecommerce.generators.seller import generate_sellers
from ecommerce.utils.faker_utils import seed_generators


def generate_reference_data():
    seed_generators(42)

    brands = generate_brands()
    categories = generate_categories()
    sellers = generate_sellers()

    return brands, categories, sellers


def test_generate_3000_products():
    brands, categories, sellers = generate_reference_data()

    products = generate_products(
        brands,
        categories,
        sellers,
    )

    assert len(products) == 3000

    assert [product["product_id"] for product in products] == list(
        range(1, 3001)
    )


def test_product_foreign_keys():
    brands, categories, sellers = generate_reference_data()

    products = generate_products(
        brands,
        categories,
        sellers,
        count=100,
    )

    brand_ids = {brand["brand_id"] for brand in brands}

    category_ids = {
        category["category_id"]
        for category in categories
        if category["level"] == 2
    }

    seller_ids = {seller["seller_id"] for seller in sellers}

    for product in products:
        assert product["brand_id"] in brand_ids
        assert product["category_id"] in category_ids
        assert product["seller_id"] in seller_ids


def test_product_business_rules():
    brands, categories, sellers = generate_reference_data()

    products = generate_products(
        brands,
        categories,
        sellers,
        count=100,
    )

    for product in products:
        assert product["product_name"]
        assert len(product["product_name"]) <= 200

        assert Decimal(100000) <= product["price"] <= Decimal(50000000)
        assert isinstance(product["price"], Decimal)

        assert 0 <= product["stock_qty"] <= 500

        assert Decimal("3.0") <= product["rating"] <= Decimal("5.0")

        assert isinstance(product["is_active"], bool)


def test_product_audit_fields():
    brands, categories, sellers = generate_reference_data()

    products = generate_products(
        brands,
        categories,
        sellers,
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

    for product in products:
        assert audit_columns.issubset(product.keys())

        assert product["created_by"] == "data_generator"

        if product["updated_at"] is not None:
            assert product["updated_at"] >= product["created_at"]

        if product["is_deleted"]:
            assert product["deleted_at"] is not None
            assert product["deleted_by"] is not None

            delete_start = (
                product["updated_at"] or product["created_at"]
            )

            assert product["deleted_at"] >= delete_start
        else:
            assert product["deleted_at"] is None
            assert product["deleted_by"] is None


def test_product_created_at_range():
    brands, categories, sellers = generate_reference_data()

    products = generate_products(
        brands,
        categories,
        sellers,
        count=100,
    )

    start = datetime(2024, 6, 1)
    end = datetime(2024, 12, 31, 23, 59, 59)

    for product in products:
        assert start <= product["created_at"] <= end


def test_invalid_product_count():
    brands, categories, sellers = generate_reference_data()

    with pytest.raises(ValueError):
        generate_products(
            brands,
            categories,
            sellers,
            count=0,
        )


def test_empty_reference_data():
    brands, categories, sellers = generate_reference_data()

    with pytest.raises(ValueError):
        generate_products([], categories, sellers)

    with pytest.raises(ValueError):
        generate_products(brands, [], sellers)

    with pytest.raises(ValueError):
        generate_products(brands, categories, [])


def test_no_subcategory_available():
    brands, categories, sellers = generate_reference_data()

    main_categories = [
        category for category in categories
        if category["level"] == 1
    ]

    with pytest.raises(ValueError):
        generate_products(
            brands,
            main_categories,
            sellers,
        )