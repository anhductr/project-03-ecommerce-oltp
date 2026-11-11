-- =========================================
-- PROJECT 03: E-COMMERCE OLTP
-- Database: PostgreSQL
-- =========================================


-- 1. BRAND
CREATE TABLE brand (
    brand_id SERIAL PRIMARY KEY,
    brand_name VARCHAR(100) UNIQUE NOT NULL,
    country VARCHAR(50),
    created_at TIMESTAMP NOT NULL
);


-- 2. CATEGORY
CREATE TABLE category (
    category_id SERIAL PRIMARY KEY,
    category_name VARCHAR(100) UNIQUE NOT NULL,
    parent_category_id INT REFERENCES category(category_id),
    level SMALLINT NOT NULL CHECK (level IN (1, 2)),
    created_at TIMESTAMP NOT NULL,

    CHECK (
        (level = 1 AND parent_category_id IS NULL)
        OR
        (level = 2 AND parent_category_id IS NOT NULL)
    )
);


-- 3. SELLER
CREATE TABLE seller (
    seller_id SERIAL PRIMARY KEY,
    seller_name VARCHAR(150) NOT NULL,
    join_date DATE NOT NULL,
    seller_type VARCHAR(50) NOT NULL
        CHECK (seller_type IN ('Official', 'Marketplace')),
    rating DECIMAL(2,1)
        CHECK (rating >= 0 AND rating <= 5),
    country VARCHAR(50) NOT NULL
);


-- 4. CUSTOMER
CREATE TABLE customer (
    customer_id SERIAL PRIMARY KEY,
    customer_name VARCHAR(150) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    phone VARCHAR(20) UNIQUE NOT NULL,
    gender VARCHAR(10) NOT NULL
        CHECK (gender IN ('Male', 'Female')),
    address VARCHAR(255),
    city VARCHAR(100),
    created_at TIMESTAMP NOT NULL
);


-- 5. PRODUCT
CREATE TABLE product (
    product_id SERIAL PRIMARY KEY,
    product_name VARCHAR(200) NOT NULL,

    category_id INT NOT NULL
        REFERENCES category(category_id),

    brand_id INT NOT NULL
        REFERENCES brand(brand_id),

    seller_id INT NOT NULL
        REFERENCES seller(seller_id),

    price DECIMAL(12,2) NOT NULL
        CHECK (price > 0),

    stock_qty INT NOT NULL
        CHECK (stock_qty >= 0),

    rating DECIMAL(2,1)
        CHECK (rating >= 0 AND rating <= 5),

    created_at TIMESTAMP NOT NULL,

    is_active BOOLEAN NOT NULL DEFAULT TRUE
);


-- 6. PROMOTION
CREATE TABLE promotion (
    promotion_id SERIAL PRIMARY KEY,
    promotion_name VARCHAR(100) NOT NULL,

    promotion_type VARCHAR(50) NOT NULL,

    discount_type VARCHAR(20) NOT NULL
        CHECK (discount_type IN ('percentage', 'fixed_amount')),

    discount_value NUMERIC(10,2) NOT NULL,

    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    created_at TIMESTAMP NOT NULL,

    CHECK (
        discount_value > 0
        AND (
            discount_type = 'fixed_amount'
            OR discount_value <= 100
        )
    ),

    CHECK (start_date >= created_at::DATE),
    CHECK (end_date >= start_date)
);


-- 7. PROMOTION_PRODUCT
CREATE TABLE promotion_product (
    promo_product_id SERIAL PRIMARY KEY,

    promotion_id INT NOT NULL
        REFERENCES promotion(promotion_id),

    product_id INT NOT NULL
        REFERENCES product(product_id),

    created_at TIMESTAMP NOT NULL,

    UNIQUE (promotion_id, product_id)
);


-- =========================================
-- INDEXES FOR FOREIGN KEYS
-- =========================================

CREATE INDEX idx_category_parent
ON category(parent_category_id);

CREATE INDEX idx_product_category
ON product(category_id);

CREATE INDEX idx_product_brand
ON product(brand_id);

CREATE INDEX idx_product_seller
ON product(seller_id);

CREATE INDEX idx_promotion_product_product
ON promotion_product(product_id);

CREATE INDEX idx_promotion_product_promotion
ON promotion_product(promotion_id);