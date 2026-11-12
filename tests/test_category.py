from datetime import datetime

from ecommerce.generators.category import generate_categories
from ecommerce.utils.faker_utils import seed_generators


def test_generate_25_categories():
    seed_generators(42)

    categories = generate_categories()

    assert len(categories) == 25

    assert len({
        category["category_name"] for category in categories
    }) == 25


def test_category_levels():
    seed_generators(42)

    categories = generate_categories()

    main_categories = [
        category for category in categories
        if category["level"] == 1
    ]

    subcategories = [
        category for category in categories
        if category["level"] == 2
    ]

    assert len(main_categories) == 5
    assert len(subcategories) == 20


def test_category_relationships():
    seed_generators(42)

    categories = generate_categories()

    category_by_id = {
        category["category_id"]: category
        for category in categories
    }

    for category in categories:

        if category["level"] == 1:
            assert category["parent_category_id"] is None

        elif category["level"] == 2:

            parent_id = category["parent_category_id"]

            assert parent_id in category_by_id

            parent = category_by_id[parent_id]

            assert parent["level"] == 1

            assert parent["created_at"] <= category["created_at"]


def test_category_audit_fields():
    seed_generators(42)

    categories = generate_categories()

    audit_columns = {
        "created_at",
        "created_by",
        "updated_at",
        "updated_by",
        "is_deleted",
        "deleted_at",
        "deleted_by",
    }

    for category in categories:

        assert audit_columns.issubset(category.keys())

        assert category["created_by"] == "data_generator"


def test_category_created_at_range():
    seed_generators(42)

    categories = generate_categories()

    start = datetime(2024, 1, 1)
    end = datetime(2024, 12, 31, 23, 59, 59)

    for category in categories:
        assert start <= category["created_at"] <= end