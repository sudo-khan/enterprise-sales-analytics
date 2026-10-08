import pandas as pd
import numpy as np
from datetime import datetime, timedelta

np.random.seed(42)

# --- 1. Dimension: Customers ---
num_customers = 500
industries = ["Fintech", "Healthcare", "E-Commerce", "SaaS", "Logistics", "EdTech"]
tiers = ["Enterprise", "Mid-Market", "SMB"]
regions = ["EMEA", "APAC", "Americas"]

customers = []
for cid in range(1, num_customers + 1):
    customers.append({
        "customer_id": cid,
        "company_name": f"Enterprise_Client_{cid:03d}",
        "industry": np.random.choice(industries),
        "tier": np.random.choice(tiers, p=[0.2, 0.4, 0.4]),
        "region": np.random.choice(regions, p=[0.4, 0.25, 0.35]),
        "onboarding_date": (datetime(2023, 1, 1) + timedelta(days=int(np.random.randint(0, 700)))).strftime("%Y-%m-%d")
    })
df_customers = pd.DataFrame(customers)
df_customers.to_csv("data/dim_customers.csv", index=False)

# --- 2. Dimension: Products ---
products = [
    {"product_id": 101, "product_name": "Cloud Security Suite", "product_category": "Security", "unit_cost": 450.00, "base_price": 1200.00},
    {"product_id": 102, "product_name": "Analytics Enterprise Engine", "product_category": "Analytics", "unit_cost": 300.00, "base_price": 950.00},
    {"product_id": 103, "product_name": "API Gateway Pro", "product_category": "Infrastructure", "unit_cost": 150.00, "base_price": 450.00},
    {"product_id": 104, "product_name": "Workflow Automation Hub", "product_category": "Productivity", "unit_cost": 200.00, "base_price": 600.00},
    {"product_id": 105, "product_name": "Customer Data Platform", "product_category": "Analytics", "unit_cost": 500.00, "base_price": 1500.00}
]
df_products = pd.DataFrame(products)
df_products.to_csv("data/dim_products.csv", index=False)

# --- 3. Dimension: Sales Representatives ---
reps = [
    {"sales_rep_id": 1, "rep_name": "Liam O'Connor", "region": "EMEA", "quota_target": 1200000},
    {"sales_rep_id": 2, "rep_name": "Sarah Jenkins", "region": "Americas", "quota_target": 1500000},
    {"sales_rep_id": 3, "rep_name": "Kenji Sato", "region": "APAC", "quota_target": 950000},
    {"sales_rep_id": 4, "rep_name": "Amina Yusuf", "region": "EMEA", "quota_target": 1100000},
    {"sales_rep_id": 5, "rep_name": "Mateo Rossi", "region": "Americas", "quota_target": 1350000}
]
df_reps = pd.DataFrame(reps)
df_reps.to_csv("data/dim_sales_reps.csv", index=False)

# --- 4. Fact: Sales Orders (50,000 Transactions) ---
num_transactions = 50000
start_date = datetime(2024, 1, 1)

transaction_dates = [start_date + timedelta(minutes=int(np.random.randint(0, 525600))) for _ in range(num_transactions)]
transaction_dates.sort()

orders = []
for order_id, dt in enumerate(transaction_dates, start=10001):
    cust = df_customers.sample(1).iloc[0]
    prod = df_products.sample(1).iloc[0]
    rep = df_reps[df_reps['region'] == cust['region']].sample(1).iloc[0]
    
    quantity = np.random.choice([1, 2, 3, 5, 10], p=[0.45, 0.25, 0.15, 0.10, 0.05])
    discount_pct = np.random.choice([0.0, 0.05, 0.10, 0.15, 0.25], p=[0.4, 0.25, 0.2, 0.1, 0.05])
    
    gross_revenue = round(prod["base_price"] * quantity, 2)
    discount_amount = round(gross_revenue * discount_pct, 2)
    net_revenue = round(gross_revenue - discount_amount, 2)
    total_cost = round(prod["unit_cost"] * quantity, 2)
    gross_profit = round(net_revenue - total_cost, 2)
    
    orders.append({
        "order_id": order_id,
        "order_timestamp": dt.strftime("%Y-%m-%d %H:%M:%S"),
        "customer_id": cust["customer_id"],
        "product_id": prod["product_id"],
        "sales_rep_id": rep["sales_rep_id"],
        "quantity": quantity,
        "gross_revenue": gross_revenue,
        "discount_amount": discount_amount,
        "net_revenue": net_revenue,
        "total_cost": total_cost,
        "gross_profit": gross_profit,
        "status": np.random.choice(["Completed", "Completed", "Completed", "Refunded"], p=[0.92, 0.03, 0.02, 0.03])
    })

df_orders = pd.DataFrame(orders)
df_orders.to_csv("data/fact_sales_orders.csv", index=False)

print(f"Generated:")
print(f" - {len(df_customers)} Customers")
print(f" - {len(df_products)} Products")
print(f" - {len(df_reps)} Sales Reps")
print(f" - {len(df_orders):,} Transactions in data/fact_sales_orders.csv")