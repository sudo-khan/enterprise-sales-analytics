import pandas as pd
import sys

def run_validations():
    print("Running Pre-Load Data Contract Assertions...")
    
    df_orders = pd.read_csv("data/fact_sales_orders.csv")
    df_customers = pd.read_csv("data/dim_customers.csv")
    df_products = pd.read_csv("data/dim_products.csv")

    # 1. Null Checks
    assert df_orders["order_id"].isnull().sum() == 0, "Assertion Failed: Null order IDs found."
    assert df_orders["net_revenue"].isnull().sum() == 0, "Assertion Failed: Null revenue values."

    # 2. Referential Integrity
    valid_customer_ids = set(df_customers["customer_id"])
    assert set(df_orders["customer_id"]).issubset(valid_customer_ids), "Assertion Failed: Foreign key violation in customer_id."

    valid_product_ids = set(df_products["product_id"])
    assert set(df_orders["product_id"]).issubset(valid_product_ids), "Assertion Failed: Foreign key violation in product_id."

    # 3. Business Logic Bounds
    assert (df_orders["net_revenue"] >= 0).all(), "Assertion Failed: Negative revenue detected."
    assert (df_orders["quantity"] > 0).all(), "Assertion Failed: Zero or negative quantity found."

    print("All 6 Pre-Load Validation Gates Passed Cleanly!")

if __name__ == "__main__":
    run_validations()