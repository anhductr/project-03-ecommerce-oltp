# E-commerce OLTP Data Generator

A Python-based project that generates synthetic e-commerce data using Faker, validates data quality, exports datasets to CSV, and loads them into a PostgreSQL database.

The project demonstrates a basic data engineering workflow, from synthetic data generation to relational database loading and data quality verification.

## 1. Project Objectives

- Generate realistic synthetic e-commerce data using Python and Faker.
- Design a relational OLTP database schema in PostgreSQL.
- Maintain primary key and foreign key relationships.
- Implement data validation and business rules.
- Export generated datasets into CSV files.
- Perform bulk data loading using PostgreSQL COPY.
- Verify data integrity using SQL queries.

## 2. Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.12 | Data generation and pipeline development |
| Faker | Synthetic data generation |
| PostgreSQL | Relational database |
| Psycopg 3 | Python–PostgreSQL connection and data loading |
| CSV | Intermediate data storage |
| python-dotenv | Environment variable management |
| uv | Python dependency and environment management |
| pytest | Unit and data validation tests |
| Ruff | Code linting |

## 3. Database Schema

The project contains seven tables:

| Table | Expected Records | Description |
|---|---:|---|
| brand | 20 | Product brands |
| category | 25 | Product categories |
| seller | 50 | Sellers |
| customer | 30,000 | Customers |
| product | 3,000 | Products |
| promotion | 30 | Promotional campaigns |
| promotion_product | 500 | Relationships between promotions and products |
| **Total** | **33,625** | |

### Relationships

- A product belongs to a brand.
- A product belongs to a category.
- A product belongs to a seller.
- A promotion can be associated with multiple products.
- A product can participate in multiple promotions.
- Products are assigned to level-2 categories.

The schema also includes:

- Primary keys
- Foreign keys
- Unique constraints
- Check constraints
- Indexes
- Audit fields

Audit fields include `created_at`, `created_by`, `updated_at`, `updated_by`, `is_deleted`, `deleted_at`, and `deleted_by`.

## 4. Project Structure

```text
ecommerce-oltp/
├── data/
│   └── generated/
├── scripts/
│   ├── generate_data.py
│   └── load_data.py
├── sql/
│   └── schema.sql
├── src/
│   └── ecommerce/
│       ├── database/
│       │   ├── connection.py
│       │   └── loader.py
│       ├── generators/
│       └── utils/
│           ├── audit_utils.py
│           ├── faker_utils.py
│           └── validation.py
├── tests/
├── .env.example
├── .gitignore
├── pyproject.toml
├── uv.lock
└── README.md
```

## 5. Setup and Installation

### Prerequisites

- Python 3.12
- PostgreSQL
- uv

### Clone the repository

```bash
git clone https://github.com/anhductr/project-03-ecommerce-oltp.git ecommerce-oltp
cd ecommerce-oltp
```

### Install dependencies

```bash
uv sync --locked
```

### Configure environment variables

Create a local environment file:

```bash
cp .env.example .env
```

Update `.env` with your PostgreSQL connection settings:

```env
DB_HOST=127.0.0.1
DB_PORT=5432
DB_NAME=ecommerce_oltp
DB_USER=your_database_user
DB_PASSWORD=your_database_password
```

Never commit the `.env` file or expose database credentials.

### Create the database

Create the database if it does not already exist:

```sql
CREATE DATABASE ecommerce_oltp;
```

Apply the database schema:

```bash
psql -h 127.0.0.1 -U your_database_user -d ecommerce_oltp -f sql/schema.sql
```

## 6. Data Pipeline

The pipeline consists of the following stages:

```text
Python + Faker
      |
      v
Generate Synthetic Data
      |
      v
Validate Dataset
      |
      v
Export CSV Files
      |
      v
Load Data into PostgreSQL
      |
      v
Data Quality Verification
```

### Step 1: Generate and validate data

```bash
uv run python scripts/generate_data.py
```

This step:

- Generates data for seven tables.
- Validates expected record counts.
- Checks foreign key relationships and business rules.
- Validates audit fields.
- Exports datasets into `data/generated/`.

### Step 2: Load data into PostgreSQL

```bash
uv run python scripts/load_data.py
```

The loader:

- Reads CSV files.
- Connects to PostgreSQL using Psycopg.
- Loads data using PostgreSQL COPY.
- Loads tables in foreign-key dependency order.
- Synchronizes sequences where applicable.
- Reports the number of records loaded.

**Important:** The loader performs a full refresh of the seven target tables. It truncates existing data before loading the CSV files. Run it only when replacing those datasets is intended.

### Step 3: Verify loaded data

Connect to PostgreSQL:

```bash
psql -h 127.0.0.1 -U your_database_user -d ecommerce_oltp
```

Check record counts:

```sql
SELECT 'brand' AS table_name, COUNT(*) AS total_rows FROM brand
UNION ALL
SELECT 'category', COUNT(*) FROM category
UNION ALL
SELECT 'seller', COUNT(*) FROM seller
UNION ALL
SELECT 'customer', COUNT(*) FROM customer
UNION ALL
SELECT 'product', COUNT(*) FROM product
UNION ALL
SELECT 'promotion', COUNT(*) FROM promotion
UNION ALL
SELECT 'promotion_product', COUNT(*) FROM promotion_product
ORDER BY table_name;
```

Additional data quality checks include:

- Foreign key integrity.
- Duplicate promotion-product relationships.
- Product category hierarchy.
- Audit field consistency.

## 7. Testing and Code Quality

Run unit tests:

```bash
uv run pytest -v
```

Run Ruff:

```bash
uv run ruff check .
```

Check Python syntax:

```bash
uv run python -m compileall -q src scripts tests
```

## 8. Project Results

The pipeline successfully generated and loaded **33,625 records** across seven PostgreSQL tables.

Data verification results:

| Validation | Result |
|---|---|
| Expected record counts | PASS |
| Product foreign key integrity | PASS |
| Promotion-product foreign key integrity | PASS |
| Duplicate promotion-product pairs | 0 duplicates |
| Invalid product categories | 0 |
| Invalid audit records | 0 across all seven tables |

## 9. Key Learnings

Through this project, I practiced:

- Python data generation with Faker.
- Relational database design.
- Primary key and foreign key management.
- Data validation and business rules.
- CSV data processing.
- PostgreSQL connectivity using Psycopg.
- Bulk data loading with PostgreSQL COPY.
- SQL-based data quality verification.
- Python testing and code quality.
- Dependency and environment management with uv.