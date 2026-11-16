from ecommerce.database.loader import load_data


def main() -> None:
    print("=" * 50)
    print("START LOADING DATA INTO POSTGRESQL")
    print("=" * 50)

    row_counts = load_data()

    print("\n" + "=" * 50)
    print("DATA LOADING SUMMARY")
    print("=" * 50)

    total_rows = 0

    for table_name, count in row_counts.items():
        print(f"{table_name:<25} {count:>10,}")
        total_rows += count

    print("-" * 50)
    print(f"{'TOTAL':<25} {total_rows:>10,}")
    print("=" * 50)

    print("\nData loading completed successfully!")


if __name__ == "__main__":
    main()