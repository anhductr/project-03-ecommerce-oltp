from datetime import datetime


EXPECTED_COUNTS = {
    "brand": 20,
    "category": 25,
    "seller": 50,
    "customer": 30_000,
    "product": 3_000,
    "promotion": 30,
    "promotion_product": 500,
}


AUDIT_COLUMNS = {
    "created_at",
    "created_by",
    "updated_at",
    "updated_by",
    "is_deleted",
    "deleted_at",
    "deleted_by",
}


def validate_unique(
    records: list[dict[str, object]],
    column: str,
    table_name: str,
) -> None:
    values = [record[column] for record in records]

    if len(values) != len(set(values)):
        raise ValueError(f"Duplicate values in {table_name}.{column}")


def validate_audit(
    records: list[dict[str, object]],
    table_name: str,
) -> None:
    for record in records:
        if not AUDIT_COLUMNS.issubset(record.keys()):
            raise ValueError(f"Missing audit columns in {table_name}")

        created_at = record["created_at"]
        created_by = record["created_by"]

        if not isinstance(created_at, datetime):
            raise ValueError(f"Invalid created_at in {table_name}")

        if not created_by or len(created_by) > 20:
            raise ValueError(f"Invalid created_by in {table_name}")

        updated_at = record["updated_at"]
        updated_by = record["updated_by"]

        if updated_at is None:
            if updated_by is not None:
                raise ValueError(f"Invalid update audit in {table_name}")
        else:
            if (
                not isinstance(updated_at, datetime)
                or not updated_by
                or len(updated_by) > 20
                or updated_at < created_at
            ):
                raise ValueError(f"Invalid update audit in {table_name}")

        is_deleted = record["is_deleted"]
        deleted_at = record["deleted_at"]
        deleted_by = record["deleted_by"]

        if not isinstance(is_deleted, bool):
            raise ValueError(f"Invalid is_deleted in {table_name}")

        if is_deleted:
            delete_start = updated_at or created_at

            if (
                not isinstance(deleted_at, datetime)
                or not deleted_by
                or len(deleted_by) > 20
                or deleted_at < delete_start
            ):
                raise ValueError(f"Invalid delete audit in {table_name}")

        elif deleted_at is not None or deleted_by is not None:
            raise ValueError(f"Invalid delete audit in {table_name}")


def validate_dataset(
    dataset: dict[str, list[dict[str, object]]],
) -> None:
    """
    Validate row counts, unique constraints,
    foreign keys, business rules and audit fields.
    """

    # 1. Validate row counts
    for table_name, expected_count in EXPECTED_COUNTS.items():

        records = dataset.get(table_name)

        if records is None:
            raise ValueError(f"Missing table: {table_name}")

        if len(records) != expected_count:
            raise ValueError(
                f"{table_name}: expected {expected_count} rows, "
                f"got {len(records)}"
            )

        validate_audit(records, table_name)

    # 2. Validate unique columns
    validate_unique(dataset["brand"], "brand_id", "brand")
    validate_unique(dataset["brand"], "brand_name", "brand")

    validate_unique(dataset["category"], "category_id", "category")
    validate_unique(dataset["category"], "category_name", "category")

    validate_unique(dataset["seller"], "seller_id", "seller")

    validate_unique(dataset["customer"], "customer_id", "customer")
    validate_unique(dataset["customer"], "email", "customer")
    validate_unique(dataset["customer"], "phone", "customer")

    validate_unique(dataset["product"], "product_id", "product")
    validate_unique(dataset["promotion"], "promotion_id", "promotion")

    validate_unique(
        dataset["promotion_product"],
        "promo_product_id",
        "promotion_product",
    )

    # 3. Validate category hierarchy
    category_by_id = {
        category["category_id"]: category
        for category in dataset["category"]
    }

    main_categories = [
        category for category in dataset["category"]
        if category["level"] == 1
    ]

    subcategories = [
        category for category in dataset["category"]
        if category["level"] == 2
    ]

    if len(main_categories) != 5 or len(subcategories) != 20:
        raise ValueError("Invalid category hierarchy")

    for category in dataset["category"]:

        parent_id = category["parent_category_id"]

        if category["level"] == 1:
            if parent_id is not None:
                raise ValueError("Main category cannot have a parent")

        elif category["level"] == 2:
            parent = category_by_id.get(parent_id)

            if parent is None or parent["level"] != 1:
                raise ValueError("Invalid category parent")

            if parent["created_at"] > category["created_at"]:
                raise ValueError("Subcategory created before its parent")

    # 4. Validate product foreign keys
    brand_ids = {
        brand["brand_id"] for brand in dataset["brand"]
    }

    seller_ids = {
        seller["seller_id"] for seller in dataset["seller"]
    }

    subcategory_ids = {
        category["category_id"] for category in subcategories
    }

    for product in dataset["product"]:

        if product["brand_id"] not in brand_ids:
            raise ValueError("Invalid product brand_id")

        if product["seller_id"] not in seller_ids:
            raise ValueError("Invalid product seller_id")

        if product["category_id"] not in subcategory_ids:
            raise ValueError("Invalid product category_id")

    # 5. Validate promotion business rules
    for promotion in dataset["promotion"]:

        if promotion["promotion_type"] not in {
            "product", "category", "seller", "flash_sale"
        }:
            raise ValueError("Invalid promotion_type")

        discount_type = promotion["discount_type"]
        discount_value = promotion["discount_value"]

        if discount_value <= 0:
            raise ValueError("Invalid discount_value")

        if discount_type == "percentage":
            if discount_value > 100:
                raise ValueError("Percentage discount cannot exceed 100")

        elif discount_type != "fixed_amount":
            raise ValueError("Invalid discount_type")

        start_date = promotion["start_date"]
        end_date = promotion["end_date"]

        if start_date < promotion["created_at"].date():
            raise ValueError("Promotion starts before it was created")

        if end_date < start_date:
            raise ValueError("Promotion end_date before start_date")

        duration = (end_date - start_date).days

        if not 30 <= duration <= 50:
            raise ValueError("Invalid promotion duration")

    # 6. Validate promotion_product foreign keys and uniqueness
    promotion_by_id = {
        promotion["promotion_id"]: promotion
        for promotion in dataset["promotion"]
    }

    product_by_id = {
        product["product_id"]: product
        for product in dataset["product"]
    }

    valid_promotion_ids = {
        promotion["promotion_id"]
        for promotion in dataset["promotion"]
        if not promotion["is_deleted"]
    }

    valid_product_ids = {
        product["product_id"]
        for product in dataset["product"]
        if not product["is_deleted"] and product["is_active"]
    }

    pairs = []

    for item in dataset["promotion_product"]:

        promotion_id = item["promotion_id"]
        product_id = item["product_id"]

        if promotion_id not in valid_promotion_ids:
            raise ValueError("Invalid promotion_product promotion_id")

        if product_id not in valid_product_ids:
            raise ValueError("Invalid promotion_product product_id")

        pairs.append((promotion_id, product_id))

        promotion = promotion_by_id[promotion_id]
        product = product_by_id[product_id]

        earliest_created_at = max(
            datetime(2025, 1, 1),
            promotion["created_at"],
            product["created_at"],
        )

        if item["created_at"] < earliest_created_at:
            raise ValueError("Invalid promotion_product created_at")

    if len(pairs) != len(set(pairs)):
        raise ValueError("Duplicate promotion-product pairs")

    print("Data validation successful!")