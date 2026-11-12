from datetime import datetime

from ecommerce.utils.audit_utils import generate_audit_fields
from ecommerce.utils.faker_utils import (
    fake_vi,
    random_choice,
    random_datetime,
)

# =========================================
# CUSTOMER CONFIGURATION
# =========================================

CUSTOMER_COUNT = 30_000

GENDERS = ["Male", "Female"]

VN_MOBILE_PREFIXES = [
    "032", "033", "034", "035", "036", "037",
    "038", "039", "056", "058", "070", "076",
    "077", "078", "079", "081", "082", "083",
    "084", "085", "086", "088", "089", "090",
    "091", "092", "093", "094", "096", "097",
    "098", "099",
]

CREATED_START = datetime(2024, 1, 1)

CREATED_END = datetime(2024, 12, 31, 23, 59, 59)

PROJECT_AS_OF = datetime(2025, 5, 31, 23, 59, 59)


# =========================================
# CUSTOMER GENERATOR
# =========================================

def generate_customers(
    count: int = CUSTOMER_COUNT,
) -> list[dict[str, object]]:
    """
    Generate synthetic Vietnamese customers.
    """

    if count <= 0:
        raise ValueError("count must be greater than 0")

    customers = []

    used_emails = set()
    used_phones = set()

    for customer_id in range(1, count + 1):

        # Generate unique email
        base_email = fake_vi.email().strip().lower()

        local_part = base_email.split("@", 1)[0]

        email_suffix = f".{customer_id}@example.com"

        max_local_length = 150 - len(email_suffix)

        email = f"{local_part[:max_local_length]}{email_suffix}"

        if email in used_emails:
            raise RuntimeError(f"Duplicate email generated: {email}")

        used_emails.add(email)

        # Generate unique Vietnamese phone number
        for _ in range(100):
            prefix = random_choice(VN_MOBILE_PREFIXES)

            phone = prefix + fake_vi.numerify("#######")

            if phone not in used_phones:
                used_phones.add(phone)
                break
        else:
            raise RuntimeError("Unable to generate unique phone")

        # Generate customer information
        customer_name = fake_vi.name().strip()

        address = " ".join(fake_vi.address().split())[:255]

        city = fake_vi.city()[:100]

        created_at = random_datetime(
            CREATED_START,
            CREATED_END,
        )

        customer = {
            "customer_id": customer_id,
            "customer_name": customer_name,
            "email": email,
            "phone": phone,
            "gender": random_choice(GENDERS),
            "address": address,
            "city": city,

            **generate_audit_fields(
                created_at=created_at,
                as_of=PROJECT_AS_OF,
            ),
        }

        customers.append(customer)

    return customers