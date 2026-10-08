# Enterprise Sales & Revenue Optimization Pipeline 📊

## Overview
A production-grade analytics engineering data warehouse modeling **50,000+** B2B SaaS sales transactions across multi-regional enterprise tiers. Built to maintain consistent KPI governance, track month-over-month (MoM) revenue trajectory, monitor gross margin compression, and evaluate sales representative quota attainment.

## Architecture & Data Flow
1. **Raw Ingestion & Mock Generation:** Multi-table synthetic relational data generator simulating customers, products, sales reps, and transactional order events with temporal variability.
2. **Pre-Load Data Contract (`tests/validate_raw_data.py`):** Pre-flight assertion suite validating primary/foreign key referential integrity, null thresholds, and business logic boundary conditions before ingestion.
3. **Data Warehousing (PostgreSQL):** Star-schema dimensional modeling (`dim_customers`, `dim_products`, `dim_sales_reps`, `fact_sales_orders`) with b-tree indexing on foreign keys and timestamps.
4. **Semantic & Metrics Layer (`sql/analytics_models.sql`):** dbt-style modular SQL models utilizing Common Table Expressions (CTEs), `LAG()` window functions, and dynamic margin health flags (`ALERT: Margin Compression`, `High Growth`).
5. **Visual Intelligence (`src/visualize_revenue.py`):** Executive-level visualization tracking revenue distribution across customer tiers and margin realization across industry verticals.

## Key Insights
* **Margin Compression Risk:** Tracked customer tiers experiencing greater than **300 bps** drop in gross margins month-over-month, isolating discount-heavy quarters.
* **Tier Performance:** Enterprise-tier accounts accounted for over **45%** of net revenue, driven predominantly by Cloud Security and Analytics Engine product suites.

## Repository Structure

git init
