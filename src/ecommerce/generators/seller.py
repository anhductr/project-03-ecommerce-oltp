from datetime import date, datetime, time

from ecommerce.utils.audit_utils import generate_audit_fields
from ecommerce.utils.faker_utils import (
    fake_vi,
    random_choice,
    random_date,
    random_datetime,
    random_decimal,
)

# =========================================
# SELLER CONFIGURATION
# =========================================

SELLER_COUNT = 50

SELLER_TYPES = [
    "Official",
    "Marketplace",
]

CREATED_START = date(2024, 1, 1)
CREATED_END = date(2024, 12, 31)

PROJECT_AS_OF = datetime(2025, 5, 31, 23, 59, 59)


# =========================================
# SELLER GENERATOR
# =========================================

def generate_sellers(
    count: int = SELLER_COUNT,
) -> list[dict[str, object]]:
    """
    Generate synthetic Vietnamese sellers.
    """

    if count <= 0:
        raise ValueError("count must be greater than 0")

    sellers = []
    used_names = set()

    attempts = 0
    max_attempts = count * 20

    while len(sellers) < count:

        attempts += 1

        if attempts > max_attempts:
            raise RuntimeError(
                "Unable to generate enough unique seller names"
            )

        seller_name = fake_vi.company().strip()

        if not seller_name or len(seller_name) > 150:
            continue

        if seller_name in used_names:
            continue

        used_names.add(seller_name)

        # Generate seller join date
        join_date = random_date(
            CREATED_START,
            CREATED_END,
        )

        # Generate created_at on the same day as join_date
        created_at = random_datetime(
            datetime.combine(join_date, time.min),
            datetime.combine(join_date, time(23, 59, 59)),
        )

        seller = {
            "seller_id": len(sellers) + 1,
            "seller_name": seller_name,
            "join_date": join_date,
            "seller_type": random_choice(SELLER_TYPES),
            "rating": random_decimal(3, 5, 1),
            "country": "Vietnam",

            **generate_audit_fields(
                created_at=created_at,
                as_of=PROJECT_AS_OF,
            ),
        }

        sellers.append(seller)

    return sellers