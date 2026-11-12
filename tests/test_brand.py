import pytest

from ecommerce.generators.brand import generate_brands
from ecommerce.utils.faker_utils import seed_generators


def test_generate_20_brands():
    seed_generators(42)

    brands = generate_brands()

    assert len(brands) == 20

    assert len({
        brand["brand_name"] for brand in brands
    }) == 20

    assert [brand["brand_id"] for brand in brands] == list(
        range(1, 21)
    )


def test_brand_audit_fields():
    seed_generators(42)

    brands = generate_brands()

    audit_columns = {
        "created_at",
        "created_by",
        "updated_at",
        "updated_by",
        "is_deleted",
        "deleted_at",
        "deleted_by",
    }

    for brand in brands:
        assert audit_columns.issubset(brand.keys())

        assert brand["created_by"] == "data_generator"

        if brand["is_deleted"]:
            assert brand["deleted_at"] is not None
            assert brand["deleted_by"] is not None
        else:
            assert brand["deleted_at"] is None
            assert brand["deleted_by"] is None


def test_invalid_brand_count():
    with pytest.raises(ValueError):
        generate_brands(count=0)