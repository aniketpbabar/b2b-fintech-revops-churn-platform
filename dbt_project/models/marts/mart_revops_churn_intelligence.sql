WITH merchant_metrics AS (
    SELECT * FROM {{ ref('int_merchant_metrics') }}
)
SELECT
    merchant_tier,
    quota_status,
    COUNT(merchant_id) AS total_merchants,
    SUM(gpv_monthly) AS total_monthly_gpv,
    AVG(quota_attainment_pct) AS avg_quota_attainment,
    SUM(is_churned) AS churned_merchants,
    CAST(SUM(is_churned) AS FLOAT) / COUNT(merchant_id) AS churn_rate
FROM merchant_metrics
GROUP BY merchant_tier, quota_status;
