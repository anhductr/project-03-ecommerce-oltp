from datetime import date, datetime, time

from ecommerce.utils.audit_utils import generate_audit_fields
from ecommerce.utils.faker_utils import (
    random_choice,
    random_date,
    random_datetime,
    random_decimal,
    random_int,
)

# =========================================
# PROMOTION CONFIGURATION
# =========================================

PROMOTION_COUNT = 30

PROMOTION_TYPES = [
    "product",
    "category",
    "seller",
    "flash_sale",
]

DISCOUNT_TYPES = [
    "percentage",
    "fixed_amount",
]

CAMPAIGN_NAMES = [
    "New Year Mega Sale",
    "Tet Holiday Sale",
    "Valentine Special",
    "Spring Shopping Festival",
    "Women's Day Sale",
    "Mid-Year Sale",
    "Super Brand Day",
    "Summer Shopping Festival",
    "Mega Shopping Sale",
    "Flash Sale Festival",
]

START_DATE_MIN = date(2025, 1, 1)
START_DATE_MAX = date(2025, 4, 30)

CREATED_START = datetime(2024, 12, 1)

PROJECT_AS_OF = datetime(2025, 5, 31, 23, 59, 59)


# =========================================
# PROMOTION GENERATOR
# =========================================

def generate_promotions(
    count: int = PROMOTION_COUNT,
) -> list[dict[str, object]]:
    """
    Generate synthetic E-commerce promotions.
    """

    if count <= 0:
        raise ValueError("count must be greater than 0")

    promotions = []

    for promotion_id in range(1, count + 1):

        # Generate campaign dates
        start_date = random_date(
            START_DATE_MIN,
            START_DATE_MAX,
        )

        duration = random_int(30, 50)

        end_date = date.fromordinal(
            start_date.toordinal() + duration
        )

        # Generate record creation timestamp
        created_at = random_datetime(
            CREATED_START,
            datetime.combine(start_date, time.min),
        )

        # Generate discount information
        discount_type = random_choice(DISCOUNT_TYPES)

        if discount_type == "percentage":
            discount_value = random_decimal(5, 90, 2)
        else:
            discount_value = random_decimal(10_000, 100_000, 2)

        promotion = {
            "promotion_id": promotion_id,
            "promotion_name": (
                f"{random_choice(CAMPAIGN_NAMES)} #{promotion_id:02d}"
            ),
            "promotion_type": random_choice(PROMOTION_TYPES),
            "discount_type": discount_type,
            "discount_value": discount_value,
            "start_date": start_date,
            "end_date": end_date,

            **generate_audit_fields(
                created_at=created_at,
                as_of=PROJECT_AS_OF,
            ),
        }

        promotions.append(promotion)

    return promotions