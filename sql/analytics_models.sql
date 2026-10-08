-- ====================================================================
-- MODEL 1: Monthly Cohort MoM Growth & Margin Compression Tracking
-- ====================================================================
WITH monthly_sales AS (
    SELECT 
        DATE_TRUNC('month', order_timestamp)::DATE AS sales_month,
        c.tier AS customer_tier,
        COUNT(f.order_id) AS total_orders,
        SUM(f.net_revenue) AS total_net_revenue,
        SUM(f.gross_profit) AS total_gross_profit,
        ROUND((SUM(f.gross_profit) / NULLIF(SUM(f.net_revenue), 0)) * 100, 2) AS gross_margin_pct
    FROM fact_sales_orders f
    JOIN dim_customers c ON f.customer_id = c.customer_id
    WHERE f.status = 'Completed'
    GROUP BY 1, 2
),
mom_metrics AS (
    SELECT 
        sales_month,
        customer_tier,
        total_orders,
        total_net_revenue,
        total_gross_profit,
        gross_margin_pct,
        LAG(total_net_revenue, 1) OVER (PARTITION BY customer_tier ORDER BY sales_month) AS prev_month_revenue,
        LAG(gross_margin_pct, 1) OVER (PARTITION BY customer_tier ORDER BY sales_month) AS prev_month_margin
    FROM monthly_sales
)
SELECT 
    sales_month,
    customer_tier,
    total_net_revenue,
    gross_margin_pct,
    ROUND(((total_net_revenue - prev_month_revenue) / NULLIF(prev_month_revenue, 0)) * 100, 2) AS revenue_mom_pct_change,
    ROUND((gross_margin_pct - prev_month_margin), 2) AS margin_bps_delta,
    CASE 
        WHEN (gross_margin_pct - prev_month_margin) < -3.00 THEN 'ALERT: Margin Compression'
        WHEN ((total_net_revenue - prev_month_revenue) / NULLIF(prev_month_revenue, 0)) * 100 > 15.0 THEN 'High Growth'
        ELSE 'Normal'
    END AS cohort_health_status
FROM mom_metrics
ORDER BY customer_tier, sales_month DESC;


-- ====================================================================
-- MODEL 2: Rep Quota Attainment & Product Category Profitability
-- ====================================================================
WITH rep_performance AS (
    SELECT 
        r.rep_name,
        r.region,
        r.quota_target,
        p.product_category,
        SUM(f.net_revenue) AS category_revenue,
        SUM(f.gross_profit) AS category_profit,
        DENSE_RANK() OVER (PARTITION BY r.region ORDER BY SUM(f.net_revenue) DESC) AS regional_rank
    FROM fact_sales_orders f
    JOIN dim_sales_reps r ON f.sales_rep_id = r.sales_rep_id
    JOIN dim_products p ON f.product_id = p.product_id
    WHERE f.status = 'Completed'
    GROUP BY r.rep_name, r.region, r.quota_target, p.product_category
)
SELECT 
    rep_name,
    region,
    product_category,
    category_revenue,
    category_profit,
    ROUND((category_revenue / quota_target) * 100, 2) AS quota_attainment_pct,
    regional_rank
FROM rep_performance
ORDER BY region, regional_rank, category_revenue DESC;