import random
from collections.abc import Sequence
from datetime import date, datetime
from decimal import ROUND_HALF_UP, Decimal

from faker import Faker

# =========================================
# FAKER INSTANCES
# =========================================

fake_vi = Faker("vi_VN")
fake_en = Faker("en_US")


# =========================================
# RANDOM SEED
# =========================================

def seed_generators(seed: int = 42) -> None:
    """
    Set random seed for reproducible data generation.
    """
    random.seed(seed)

    fake_vi.seed_instance(seed)
    fake_en.seed_instance(seed)


# =========================================
# RANDOM UTILITIES
# =========================================


def random_choice[T](items: Sequence[T]) -> T:
    """
    Randomly select one item from a sequence.
    """
    if not items:
        raise ValueError("Cannot choose from an empty sequence")

    return random.choice(items)


def random_int(min_value: int, max_value: int) -> int:
    """
    Generate a random integer between min_value and max_value.
    """
    if min_value > max_value:
        raise ValueError("min_value cannot be greater than max_value")

    return random.randint(min_value, max_value)


def random_decimal(
    min_value: float | Decimal,
    max_value: float | Decimal,
    decimal_places: int = 2,
) -> Decimal:
    """
    Generate a random Decimal with the specified precision.
    """
    if min_value > max_value:
        raise ValueError("min_value cannot be greater than max_value")

    if decimal_places < 0:
        raise ValueError("decimal_places cannot be negative")

    value = Decimal(
        str(random.uniform(float(min_value), float(max_value)))
    )

    precision = Decimal(1).scaleb(-decimal_places)

    return value.quantize(
        precision,
        rounding=ROUND_HALF_UP,
    )


def random_bool(probability: float = 0.5) -> bool:
    """
    Generate a random boolean based on probability.
    """
    if not 0 <= probability <= 1:
        raise ValueError("probability must be between 0 and 1")

    return random.random() < probability


# =========================================
# DATE AND DATETIME UTILITIES
# =========================================

def random_date(start_date: date, end_date: date) -> date:
    """
    Generate a random date within the given range.
    """
    if start_date > end_date:
        raise ValueError("start_date cannot be after end_date")

    return fake_en.date_between(
        start_date=start_date,
        end_date=end_date,
    )


def random_datetime(
    start_datetime: datetime,
    end_datetime: datetime,
) -> datetime:
    """
    Generate a random datetime within the given range.
    """
    if start_datetime > end_datetime:
        raise ValueError("start_datetime cannot be after end_datetime")

    return fake_en.date_time_between(
        start_date=start_datetime,
        end_date=end_datetime,
    )