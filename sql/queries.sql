-- 1. Top 5 funds by AUM
SELECT 
    f.scheme_name,
    f.fund_house,
    a.aum
FROM fact_aum a
JOIN dim_fund f 
    ON a.amfi_code = f.amfi_code
ORDER BY a.aum DESC
LIMIT 5;


-- 2. Average NAV per month
SELECT
    f.scheme_name,
    d.year,
    d.month,
    ROUND(AVG(n.nav), 2) AS average_nav
FROM fact_nav n
JOIN dim_fund f 
    ON n.amfi_code = f.amfi_code
JOIN dim_date d 
    ON n.date_key = d.date_key
GROUP BY f.scheme_name, d.year, d.month
ORDER BY d.year, d.month;


-- 3. SIP YoY growth
SELECT
    d.year,
    SUM(t.amount) AS sip_amount
FROM fact_transactions t
JOIN dim_date d 
    ON t.date_key = d.date_key
WHERE t.transaction_type = 'SIP'
GROUP BY d.year
ORDER BY d.year;


-- 4. Transactions by state
SELECT
    state,
    COUNT(*) AS total_transactions,
    SUM(amount) AS total_amount
FROM fact_transactions
GROUP BY state
ORDER BY total_amount DESC;


-- 5. Funds with expense ratio below 1%
SELECT
    f.scheme_name,
    f.fund_house,
    p.expense_ratio
FROM fact_performance p
JOIN dim_fund f 
    ON p.amfi_code = f.amfi_code
WHERE p.expense_ratio < 1
ORDER BY p.expense_ratio;


-- 6. Top funds by 1-year return
SELECT
    f.scheme_name,
    f.fund_house,
    p.return_1y
FROM fact_performance p
JOIN dim_fund f 
    ON p.amfi_code = f.amfi_code
ORDER BY p.return_1y DESC
LIMIT 10;


-- 7. Total transaction amount by transaction type
SELECT
    transaction_type,
    COUNT(*) AS transaction_count,
    SUM(amount) AS total_amount
FROM fact_transactions
GROUP BY transaction_type;


-- 8. Average expense ratio by fund house
SELECT
    f.fund_house,
    ROUND(AVG(p.expense_ratio), 2) AS avg_expense_ratio
FROM fact_performance p
JOIN dim_fund f 
    ON p.amfi_code = f.amfi_code
GROUP BY f.fund_house
ORDER BY avg_expense_ratio;


-- 9. NAV trend for each fund by year
SELECT
    f.scheme_name,
    d.year,
    ROUND(AVG(n.nav), 2) AS avg_yearly_nav
FROM fact_nav n
JOIN dim_fund f 
    ON n.amfi_code = f.amfi_code
JOIN dim_date d 
    ON n.date_key = d.date_key
GROUP BY f.scheme_name, d.year
ORDER BY f.scheme_name, d.year;


-- 10. KYC status distribution
SELECT
    kyc_status,
    COUNT(*) AS investor_transactions
FROM fact_transactions
GROUP BY kyc_status;