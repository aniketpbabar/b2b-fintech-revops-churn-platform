WITH staged AS (
    SELECT * FROM {{ ref('stg_merchants') }}
)
SELECT
    merchant_id,
    merchant_tier,
    gpv_monthly,
    (gpv_monthly * 12) AS annualized_gpv,
    quota_attainment_pct,
    tenure_months,
    (support_tickets_30d + (failed_payouts_30d * 2)) AS risk_factor_score,
    CASE 
        WHEN quota_attainment_pct >= 1.0 THEN 'Target Achieved'
        WHEN quota_attainment_pct >= 0.8 THEN 'At Risk'
        ELSE 'Underperforming'
    END AS quota_status,
    is_churned
FROM staged;
