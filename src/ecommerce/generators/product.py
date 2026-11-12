from datetime import datetime

from ecommerce.utils.audit_utils import generate_audit_fields
from ecommerce.utils.faker_utils import (
    fake_en,
    random_bool,
    random_choice,
    random_datetime,
    random_decimal,
    random_int,
)

# =========================================
# PRODUCT CONFIGURATION
# =========================================

PRODUCT_COUNT = 3_000

PRICE_MIN = 100_000
PRICE_MAX = 50_000_000

STOCK_MIN = 0
STOCK_MAX = 500

RATING_MIN = 3
RATING_MAX = 5

CREATED_START = datetime(2024, 6, 1)

CREATED_END = datetime(2024, 12, 31, 23, 59, 59)

PROJECT_AS_OF = datetime(2025, 5, 31, 23, 59, 59)


# =========================================
# PRODUCT GENERATOR
# =========================================

def generate_products(
    brands: list[dict[str, object]],
    categories: list[dict[str, object]],
    sellers: list[dict[str, object]],
    count: int = PRODUCT_COUNT,
) -> list[dict[str, object]]:
    """
    Generate synthetic E-commerce products.

    Each product references:
    - One brand
    - One sub-category
    - One seller
    """

    if count <= 0:
        raise ValueError("count must be greater than 0")

    if not brands:
        raise ValueError("brands cannot be empty")

    if not categories:
        raise ValueError("categories cannot be empty")

    if not sellers:
        raise ValueError("sellers cannot be empty")

    # Extract valid foreign keys

    brand_ids = [
        brand["brand_id"]
        for brand in brands
    ]

    category_ids = [
        category["category_id"]
        for category in categories
        if category["level"] == 2
    ]

    seller_ids = [
        seller["seller_id"]
        for seller in sellers
    ]

    if not brand_ids:
        raise ValueError("No valid brand IDs found")

    if not category_ids:
        raise ValueError("No sub-category IDs found")

    if not seller_ids:
        raise ValueError("No valid seller IDs found")

    # Generate products

    products = []

    for product_id in range(1, count + 1):

        created_at = random_datetime(
            CREATED_START,
            CREATED_END,
        )

        product = {
            "product_id": product_id,
            "product_name": fake_en.catch_phrase()[:200],
            "category_id": random_choice(category_ids),
            "brand_id": random_choice(brand_ids),
            "seller_id": random_choice(seller_ids),
            "price": random_decimal(
                PRICE_MIN,
                PRICE_MAX,
                2,
            ),
            "stock_qty": random_int(
                STOCK_MIN,
                STOCK_MAX,
            ),
            "rating": random_decimal(
                RATING_MIN,
                RATING_MAX,
                1,
            ),
            "is_active": random_bool(),

            **generate_audit_fields(
                created_at=created_at,
                as_of=PROJECT_AS_OF,
            ),
        }

        products.append(product)

    return products