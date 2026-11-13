import csv
from pathlib import Path

from ecommerce.generators.brand import generate_brands
from ecommerce.generators.category import generate_categories
from ecommerce.generators.customer import generate_customers
from ecommerce.generators.product import generate_products
from ecommerce.generators.promotion import generate_promotions
from ecommerce.generators.promotion_product import (
    generate_promotion_products,
)
from ecommerce.generators.seller import generate_sellers

from ecommerce.utils.faker_utils import seed_generators
from ecommerce.utils.validation import validate_dataset


# =========================================
# CONFIGURATION
# =========================================

SEED = 42

OUTPUT_DIR = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "generated"
)


# =========================================
# CSV EXPORT
# =========================================

def export_to_csv(
    table_name: str,
    records: list[dict[str, object]],
) -> Path:
    """
    Export generated records to a CSV file.
    """

    if not records:
        raise ValueError(f"No records to export: {table_name}")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    output_path = OUTPUT_DIR / f"{table_name}.csv"

    fieldnames = list(records[0].keys())

    with output_path.open(
        mode="w",
        encoding="utf-8",
        newline="",
    ) as csv_file:

        writer = csv.DictWriter(
            csv_file,
            fieldnames=fieldnames,
            extrasaction="raise",
        )

        writer.writeheader()
        writer.writerows(records)

    return output_path


# =========================================
# DATA GENERATION PIPELINE
# =========================================

def generate_dataset() -> dict[str, list[dict[str, object]]]:
    """
    Generate all 7 E-commerce tables.
    """

    # Set seed only once at the beginning
    seed_generators(SEED)

    print("\nGenerating E-commerce dataset...\n")

    brands = generate_brands()
    print(f"Brand: {len(brands):,} records")

    categories = generate_categories()
    print(f"Category: {len(categories):,} records")

    sellers = generate_sellers()
    print(f"Seller: {len(sellers):,} records")

    customers = generate_customers()
    print(f"Customer: {len(customers):,} records")

    products = generate_products(
        brands,
        categories,
        sellers,
    )
    print(f"Product: {len(products):,} records")

    promotions = generate_promotions()
    print(f"Promotion: {len(promotions):,} records")

    promotion_products = generate_promotion_products(
        promotions,
        products,
    )
    print(
        f"Promotion Product: {len(promotion_products):,} records"
    )

    return {
        "brand": brands,
        "category": categories,
        "seller": sellers,
        "customer": customers,
        "product": products,
        "promotion": promotions,
        "promotion_product": promotion_products,
    }


# =========================================
# MAIN
# =========================================

def main() -> None:

    dataset = generate_dataset()

    print("\nValidating dataset...")

    validate_dataset(dataset)

    print("\nExporting CSV files...")

    total_records = 0

    for table_name, records in dataset.items():

        output_path = export_to_csv(
            table_name,
            records,
        )

        total_records += len(records)

        print(
            f"Exported {table_name}.csv "
            f"({len(records):,} records)"
        )

    print("\n====================================")
    print("DATA GENERATION COMPLETED")
    print("====================================")
    print(f"Total records: {total_records:,}")
    print(f"Output directory: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()