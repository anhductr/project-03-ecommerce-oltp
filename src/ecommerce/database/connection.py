import psycopg

from ecommerce.config import DB_CONFIG


def get_connection() -> psycopg.Connection:
    """Tạo kết nối đến PostgreSQL."""
    return psycopg.connect(**DB_CONFIG)