from datetime import datetime

from ecommerce.utils.faker_utils import (
    random_bool,
    random_choice,
    random_datetime,
)

AUDIT_ACTORS = [
    "admin_01",
    "admin_02",
    "data_generator",
]


def generate_audit_fields(
    created_at: datetime,
    as_of: datetime,
    created_by: str = "data_generator",
    update_probability: float = 0.30,
    delete_probability: float = 0.02,
) -> dict[str, datetime | str | bool | None]:

    if created_at > as_of:
        raise ValueError("created_at cannot be after as_of")

    if not created_by or len(created_by) > 20:
        raise ValueError("created_by must contain 1-20 characters")

    if not 0 <= update_probability <= 1:
        raise ValueError("update_probability must be between 0 and 1")

    if not 0 <= delete_probability <= 1:
        raise ValueError("delete_probability must be between 0 and 1")

    # UPDATE AUDIT
    updated_at = None
    updated_by = None

    if random_bool(update_probability):
        updated_at = random_datetime(created_at, as_of)
        updated_by = random_choice(AUDIT_ACTORS)

    # DELETE AUDIT
    is_deleted = random_bool(delete_probability)

    deleted_at = None
    deleted_by = None

    if is_deleted:
        delete_start = updated_at or created_at

        deleted_at = random_datetime(delete_start, as_of)
        deleted_by = random_choice(AUDIT_ACTORS)

    return {
        "created_at": created_at,
        "created_by": created_by,
        "updated_at": updated_at,
        "updated_by": updated_by,
        "is_deleted": is_deleted,
        "deleted_at": deleted_at,
        "deleted_by": deleted_by,
    }