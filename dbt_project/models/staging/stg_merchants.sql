WITH raw_merchants AS (
    SELECT
        merchant_id,
        CAST(gpv_monthly AS NUMERIC(18, 2)) AS gpv_monthly,
        CAST(quota_attainment AS NUMERIC(5, 4)) AS quota_attainment_pct,
        CAST(tenure_months AS INT) AS tenure_months,
        CAST(support_tickets_30d AS INT) AS support_tickets_30d,
        CAST(failed_payouts_30d AS INT) AS failed_payouts_30d,
        UPPER(merchant_tier) AS merchant_tier,
        CAST(churned AS INT) AS is_churned
    FROM {{ source('raw_data', 'merchant_data') }}
)
SELECT * FROM raw_merchants;
