import os
from pathlib import Path

from dotenv import load_dotenv

# Xác định thư mục gốc của project
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Đọc biến môi trường từ file .env
load_dotenv(PROJECT_ROOT / ".env")


def get_required_env(name: str) -> str:
    """Lấy biến môi trường bắt buộc."""
    value = os.getenv(name)

    if not value:
        raise ValueError(f"Missing environment variable: {name}")

    return value


# Cấu hình kết nối PostgreSQL
DB_CONFIG = {
    "host": get_required_env("DB_HOST"),
    "port": int(os.getenv("DB_PORT", "5432")),
    "dbname": get_required_env("DB_NAME"),
    "user": get_required_env("DB_USER"),
    "password": get_required_env("DB_PASSWORD"),
}