DROP TABLE IF EXISTS fact_sales_orders CASCADE;
DROP TABLE IF EXISTS dim_customers CASCADE;
DROP TABLE IF EXISTS dim_products CASCADE;
DROP TABLE IF EXISTS dim_sales_reps CASCADE;

CREATE TABLE dim_customers (
    customer_id INT PRIMARY KEY,
    company_name VARCHAR(100) NOT NULL,
    industry VARCHAR(50) NOT NULL,
    tier VARCHAR(50) NOT NULL,
    region VARCHAR(50) NOT NULL,
    onboarding_date DATE NOT NULL
);

CREATE TABLE dim_products (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    product_category VARCHAR(50) NOT NULL,
    unit_cost NUMERIC(10,2) NOT NULL,
    base_price NUMERIC(10,2) NOT NULL
);

CREATE TABLE dim_sales_reps (
    sales_rep_id INT PRIMARY KEY,
    rep_name VARCHAR(100) NOT NULL,
    region VARCHAR(50) NOT NULL,
    quota_target NUMERIC(12,2) NOT NULL
);

CREATE TABLE fact_sales_orders (
    order_id INT PRIMARY KEY,
    order_timestamp TIMESTAMP NOT NULL,
    customer_id INT REFERENCES dim_customers(customer_id),
    product_id INT REFERENCES dim_products(product_id),
    sales_rep_id INT REFERENCES dim_sales_reps(sales_rep_id),
    quantity INT NOT NULL,
    gross_revenue NUMERIC(12,2) NOT NULL,
    discount_amount NUMERIC(12,2) NOT NULL,
    net_revenue NUMERIC(12,2) NOT NULL,
    total_cost NUMERIC(12,2) NOT NULL,
    gross_profit NUMERIC(12,2) NOT NULL,
    status VARCHAR(30) NOT NULL
);

CREATE INDEX idx_orders_timestamp ON fact_sales_orders(order_timestamp);
CREATE INDEX idx_orders_customer ON fact_sales_orders(customer_id);
CREATE INDEX idx_orders_product ON fact_sales_orders(product_id);