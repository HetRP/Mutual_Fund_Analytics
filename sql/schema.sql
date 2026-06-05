DROP TABLE IF EXISTS fact_aum;
DROP TABLE IF EXISTS fact_performance;
DROP TABLE IF EXISTS fact_transactions;
DROP TABLE IF EXISTS fact_nav;
DROP TABLE IF EXISTS dim_date;
DROP TABLE IF EXISTS dim_fund;

CREATE TABLE dim_fund (
    amfi_code INTEGER PRIMARY KEY,
    scheme_name TEXT,
    fund_house TEXT,
    category TEXT,
    sub_category TEXT,
    risk_category TEXT
);

CREATE TABLE dim_date (
    date_key INTEGER PRIMARY KEY,
    full_date DATE,
    year INTEGER,
    quarter INTEGER,
    month INTEGER,
    month_name TEXT,
    day INTEGER
);

CREATE TABLE fact_nav (
    nav_id INTEGER PRIMARY KEY AUTOINCREMENT,
    amfi_code INTEGER,
    date_key INTEGER,
    nav REAL,
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code),
    FOREIGN KEY (date_key) REFERENCES dim_date(date_key)
);

CREATE TABLE fact_transactions (
    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    amfi_code INTEGER,
    date_key INTEGER,
    investor_id TEXT,
    transaction_type TEXT,
    amount_inr REAL,
    state TEXT,
    kyc_status TEXT,
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code),
    FOREIGN KEY (date_key) REFERENCES dim_date(date_key)
);

CREATE TABLE fact_performance (
    performance_id INTEGER PRIMARY KEY AUTOINCREMENT,
    amfi_code INTEGER,
    return_1yr_pct REAL,
    return_3yr_pct REAL,
    return_5yr_pct REAL,
    expense_ratio_pct REAL,
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code)
);

CREATE TABLE fact_aum (
    aum_id INTEGER PRIMARY KEY AUTOINCREMENT,
    amfi_code INTEGER,
    date_key INTEGER,
    aum REAL,
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code),
    FOREIGN KEY (date_key) REFERENCES dim_date(date_key)
);