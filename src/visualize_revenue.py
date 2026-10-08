import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Read fact and dimensions
df_orders = pd.read_csv("data/fact_sales_orders.csv")
df_customers = pd.read_csv("data/dim_customers.csv")
df_merged = df_orders.merge(df_customers, on="customer_id")

# Filter completed orders
df_completed = df_merged[df_merged["status"] == "Completed"].copy()
df_completed["order_timestamp"] = pd.to_datetime(df_completed["order_timestamp"])
df_completed["month"] = df_completed["order_timestamp"].dt.to_period("M").dt.to_timestamp()

# Aggregate monthly net revenue by tier
monthly_tier = df_completed.groupby(["month", "tier"])["net_revenue"].sum().reset_index()

plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# Plot 1: Revenue Trajectory by Customer Tier
sns.lineplot(
    data=monthly_tier,
    x="month",
    y="net_revenue",
    hue="tier",
    marker="o",
    linewidth=2.5,
    ax=ax1
)
ax1.set_title("Monthly Net Revenue Trajectory by Customer Tier", fontsize=12, fontweight="bold", pad=12)
ax1.set_xlabel("Month", fontsize=10, fontweight="bold")
ax1.set_ylabel("Net Revenue ($)", fontsize=10, fontweight="bold")
ax1.tick_params(axis='x', rotation=45)

# Plot 2: Gross Profit Margin Distribution by Industry
industry_margins = df_completed.groupby("industry").apply(
    lambda x: (x["gross_profit"].sum() / x["net_revenue"].sum()) * 100
).reset_index(name="gross_margin_pct").sort_values(by="gross_margin_pct", ascending=False)

sns.barplot(
    data=industry_margins,
    x="gross_margin_pct",
    y="industry",
    palette="viridis",
    ax=ax2
)
ax2.set_title("Gross Margin % Realization by Industry Sector", fontsize=12, fontweight="bold", pad=12)
ax2.set_xlabel("Gross Margin %", fontsize=10, fontweight="bold")
ax2.set_ylabel("Industry", fontsize=10, fontweight="bold")

plt.tight_layout()
plt.savefig("enterprise_revenue_metrics.png", dpi=300)
print("Charts saved successfully as 'enterprise_revenue_metrics.png'")