CREATE OR REPLACE TABLE silver_company_profiles AS
SELECT 
    lpad(cik::VARCHAR, 10, '0') AS cik, -- Casting & Padding CIK
    upper(name) AS company_name,        -- Normalisasi Nama
    tickers[1] AS primary_ticker,       -- Ambil ticker pertama dari list
    exchanges[1] AS primary_exchange,
    sic::INTEGER AS sic_code,           -- Casting ke Integer
    sicDescription AS industry,
    entityType AS category,
    fiscalYearEnd AS fiscal_year_end
FROM read_json_auto('s3://config-elt-bucket/bronze/sec_data_*.json');
