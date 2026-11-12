from datetime import datetime

from ecommerce.utils.audit_utils import generate_audit_fields
from ecommerce.utils.faker_utils import random_datetime

# =========================================
# CATEGORY CONFIGURATION
# =========================================

CATEGORY_HIERARCHY = {
    "Electronics": [
        "Mobile Phones",
        "Laptops",
        "Tablets",
        "Cameras",
    ],
    "Fashion": [
        "Men's Clothing",
        "Women's Clothing",
        "Shoes",
        "Bags",
    ],
    "Home & Living": [
        "Furniture",
        "Kitchenware",
        "Home Decor",
        "Bedding",
    ],
    "Beauty & Personal Care": [
        "Skincare",
        "Makeup",
        "Haircare",
        "Fragrances",
    ],
    "Sports & Outdoors": [
        "Fitness Equipment",
        "Sportswear",
        "Camping Gear",
        "Cycling",
    ],
}


CREATED_START = datetime(2024, 1, 1)

CREATED_END = datetime(2024, 12, 31, 23, 59, 59)

PROJECT_AS_OF = datetime(2025, 5, 31, 23, 59, 59)


# =========================================
# CATEGORY GENERATOR
# =========================================

def generate_categories() -> list[dict[str, object]]:
    """
    Generate 25 categories:
    - 5 main categories
    - 20 subcategories
    """

    categories = []

    parent_ids = {}
    parent_created_dates = {}

    category_id = 1

    # =====================================
    # GENERATE MAIN CATEGORIES
    # =====================================

    for category_name in CATEGORY_HIERARCHY:

        created_at = random_datetime(
            CREATED_START,
            CREATED_END,
        )

        parent_ids[category_name] = category_id
        parent_created_dates[category_name] = created_at

        category = {
            "category_id": category_id,
            "category_name": category_name,
            "parent_category_id": None,
            "level": 1,

            **generate_audit_fields(
                created_at=created_at,
                as_of=PROJECT_AS_OF,
            ),
        }

        categories.append(category)

        category_id += 1

    # =====================================
    # GENERATE SUBCATEGORIES
    # =====================================

    for parent_name, subcategories in CATEGORY_HIERARCHY.items():

        for subcategory_name in subcategories:

            created_at = random_datetime(
                parent_created_dates[parent_name],
                CREATED_END,
            )

            category = {
                "category_id": category_id,
                "category_name": subcategory_name,
                "parent_category_id": parent_ids[parent_name],
                "level": 2,

                **generate_audit_fields(
                    created_at=created_at,
                    as_of=PROJECT_AS_OF,
                ),
            }

            categories.append(category)

            category_id += 1

    return categories