CREATE OR REPLACE TABLE AS
SELECT
company_name AS perusahaan,
primary_ticker AS kode_saham,
primary_exchange AS bursa_efek,
industry AS sektor_industri,
category AS status_operasional
-- CIK dan SIC dicoret karena LLM/User jarang butuh ini untuk tanya jawab umum
FROM silver_company_profiles
WHERE category = 'operating';
