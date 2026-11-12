from datetime import datetime

from ecommerce.utils.audit_utils import generate_audit_fields
from ecommerce.utils.faker_utils import fake_en, random_datetime

# =========================================
# BRAND CONFIGURATION
# =========================================

BRAND_COUNT = 20

CREATED_START = datetime(2024, 1, 1)

CREATED_END = datetime(2024, 12, 31, 23, 59, 59)

PROJECT_AS_OF = datetime(2025, 5, 31, 23, 59, 59)


# =========================================
# BRAND GENERATOR
# =========================================

def generate_brands(count: int = BRAND_COUNT) -> list[dict[str, object]]:
    """
    Generate synthetic brand records.
    """

    if count <= 0:
        raise ValueError("count must be greater than 0")

    brands = []
    used_names = set()

    attempts = 0
    max_attempts = count * 20

    while len(brands) < count:

        attempts += 1

        if attempts > max_attempts:
            raise RuntimeError("Unable to generate enough unique brand names")

        brand_name = fake_en.company().strip()

        if not brand_name or len(brand_name) > 100:
            continue

        if brand_name in used_names:
            continue

        used_names.add(brand_name)

        created_at = random_datetime(
            CREATED_START,
            CREATED_END,
        )

        brand = {
            "brand_id": len(brands) + 1,
            "brand_name": brand_name,
            "country": fake_en.country(),

            **generate_audit_fields(
                created_at=created_at,
                as_of=PROJECT_AS_OF,
            ),
        }

        brands.append(brand)

    return brands