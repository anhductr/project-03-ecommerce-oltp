import csv
from pathlib import Path

from psycopg import sql

from ecommerce.database.connection import get_connection

# Xác định thư mục gốc của project
PROJECT_ROOT = Path(__file__).resolve().parents[3]

# Thứ tự nạp dữ liệu theo quan hệ khóa ngoại
TABLE_LOAD_ORDER = [
    ("brand", "brand.csv", "brand_id"),
    ("category", "category.csv", "category_id"),
    ("seller", "seller.csv", "seller_id"),
    ("customer", "customer.csv", "customer_id"),
    ("product", "product.csv", "product_id"),
    ("promotion", "promotion.csv", "promotion_id"),
    ("promotion_product", "promotion_product.csv", "promo_product_id"),
]


def read_csv_header(csv_path: Path) -> list[str]:
    """Đọc tên các cột từ header của CSV."""

    with csv_path.open(
        "r",
        encoding="utf-8-sig",
        newline="",
    ) as file:
        reader = csv.reader(file)
        columns = next(reader, None)

    if not columns:
        raise ValueError(f"CSV file is empty: {csv_path}")

    columns = [column.strip() for column in columns]

    if any(not column for column in columns):
        raise ValueError(f"CSV contains an empty column name: {csv_path}")

    if len(columns) != len(set(columns)):
        raise ValueError(f"CSV contains duplicate column names: {csv_path}")

    return columns


def copy_csv_to_table(
    cursor,
    table_name: str,
    csv_path: Path,
    columns: list[str],
) -> None:
    """Sử dụng PostgreSQL COPY để nạp CSV vào bảng."""

    copy_query = sql.SQL(
        """
        COPY {} ({})
        FROM STDIN
        WITH (FORMAT CSV, HEADER TRUE)
        """
    ).format(
        sql.Identifier("public", table_name),
        sql.SQL(", ").join(
            sql.Identifier(column) for column in columns
        ),
    )

    with csv_path.open("rb") as file, cursor.copy(copy_query) as copy:
        while True:
            chunk = file.read(1024 * 1024)

            if not chunk:
                break

            copy.write(chunk)


def sync_sequence(cursor, table_name: str, primary_key: str) -> None:
    """Đồng bộ sequence sau khi nạp ID từ CSV."""

    cursor.execute(
        "SELECT pg_get_serial_sequence(%s, %s)",
        (f"public.{table_name}", primary_key),
    )

    sequence_name = cursor.fetchone()[0]

    # Một số cột ID có thể không sử dụng sequence
    if sequence_name is None:
        return

    query = sql.SQL(
        """
        SELECT setval(
            %s::regclass,
            COALESCE(MAX({}), 1),
            MAX({}) IS NOT NULL
        )
        FROM {}
        """
    ).format(
        sql.Identifier(primary_key),
        sql.Identifier(primary_key),
        sql.Identifier("public", table_name),
    )

    cursor.execute(query, (sequence_name,))


def load_data() -> dict[str, int]:
    """Nạp toàn bộ CSV vào PostgreSQL."""

    data_dir = PROJECT_ROOT / "data" / "generated"

    # Kiểm tra tất cả CSV trước khi thay đổi database
    files_to_load = []

    for table_name, filename, primary_key in TABLE_LOAD_ORDER:
        csv_path = data_dir / filename

        if not csv_path.is_file():
            raise FileNotFoundError(f"CSV file not found: {csv_path}")

        columns = read_csv_header(csv_path)

        files_to_load.append(
            (table_name, csv_path, primary_key, columns)
        )

    row_counts = {}

    # Toàn bộ quá trình nằm trong một transaction
    with get_connection() as connection, connection.cursor() as cursor:

        # Xóa dữ liệu cũ của 7 bảng trước khi nạp lại
        tables = sql.SQL(", ").join(
            sql.Identifier("public", table_name)
            for table_name, _, _ in TABLE_LOAD_ORDER
        )

        cursor.execute(
            sql.SQL(
                "TRUNCATE TABLE {} RESTART IDENTITY"
            ).format(tables)
        )

        # Nạp từng bảng theo thứ tự khóa ngoại
        for table_name, csv_path, primary_key, columns in files_to_load:

            print(f"Loading {table_name}...")

            copy_csv_to_table(
                cursor,
                table_name,
                csv_path,
                columns,
            )

            # Đồng bộ sequence nếu bảng sử dụng SERIAL/IDENTITY sequence
            sync_sequence(cursor, table_name, primary_key)

            # Kiểm tra số lượng bản ghi
            cursor.execute(
                sql.SQL("SELECT COUNT(*) FROM {}").format(
                    sql.Identifier("public", table_name)
                )
            )

            row_counts[table_name] = cursor.fetchone()[0]

            print(
                f"Loaded {table_name}: "
                f"{row_counts[table_name]:,} rows"
            )

    return row_counts