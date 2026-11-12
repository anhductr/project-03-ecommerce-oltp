from datetime import datetime
from random import sample

from ecommerce.utils.audit_utils import generate_audit_fields
from ecommerce.utils.faker_utils import random_datetime

# =========================================
# PROMOTION_PRODUCT CONFIGURATION
# =========================================

PROMOTION_PRODUCT_COUNT = 500

CREATED_START = datetime(2025, 1, 1)

PROJECT_AS_OF = datetime(2025, 5, 31, 23, 59, 59)


# =========================================
# PROMOTION_PRODUCT GENERATOR
# =========================================

def generate_promotion_products(
    promotions: list[dict[str, object]],
    products: list[dict[str, object]],
    count: int = PROMOTION_PRODUCT_COUNT,
) -> list[dict[str, object]]:
    """
    Generate unique promotion-product relationships.

    Each promotion can apply to multiple products.
    Each product can belong to multiple promotions.
    """

    if count <= 0:
        raise ValueError("count must be greater than 0")

    if not promotions:
        raise ValueError("promotions cannot be empty")

    if not products:
        raise ValueError("products cannot be empty")

    # Exclude soft-deleted promotions and products
    # to avoid creating new relationships with deleted records.

    valid_promotions = [
        promotion
        for promotion in promotions
        if not promotion["is_deleted"]
    ]

    valid_products = [
        product
        for product in products
        if not product["is_deleted"] and product["is_active"]
    ]

    if not valid_promotions:
        raise ValueError("No active promotions available")

    if not valid_products:
        raise ValueError("No active products available")

    # Extract IDs
    promotion_ids = [
        promotion["promotion_id"]
        for promotion in valid_promotions
    ]

    product_ids = [
        product["product_id"]
        for product in valid_products
    ]

    # Validate unique source IDs
    if len(promotion_ids) != len(set(promotion_ids)):
        raise ValueError("Duplicate promotion IDs found")

    if len(product_ids) != len(set(product_ids)):
        raise ValueError("Duplicate product IDs found")

    # Create all possible unique combinations
    possible_pairs = [
        (promotion_id, product_id)
        for promotion_id in promotion_ids
        for product_id in product_ids
    ]

    if count > len(possible_pairs):
        raise ValueError(
            f"Cannot generate {count} unique pairs. "
            f"Only {len(possible_pairs)} combinations available."
        )

    # Randomly select unique combinations
    selected_pairs = sample(possible_pairs, count)

    promotion_by_id = {
        promotion["promotion_id"]: promotion
        for promotion in valid_promotions
    }

    product_by_id = {
        product["product_id"]: product
        for product in valid_products
    }

    promotion_products = []

    for promo_product_id, (promotion_id, product_id) in enumerate(
        selected_pairs,
        start=1,
    ):

        promotion = promotion_by_id[promotion_id]
        product = product_by_id[product_id]

        # Relationship cannot be created before
        # both source records exist.
        created_start = max(
            CREATED_START,
            promotion["created_at"],
            product["created_at"],
        )

        if created_start > PROJECT_AS_OF:
            raise ValueError(
                "Source records were created after the project cutoff"
            )

        created_at = random_datetime(
            created_start,
            PROJECT_AS_OF,
        )

        promotion_product = {
            "promo_product_id": promo_product_id,
            "promotion_id": promotion_id,
            "product_id": product_id,

            **generate_audit_fields(
                created_at=created_at,
                as_of=PROJECT_AS_OF,
            ),
        }

        promotion_products.append(promotion_product)

    return promotion_products