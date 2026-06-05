# Data Dictionary

## dim_fund

| Column | Data Type | Business Meaning | Source |
|---|---|---|---|
| amfi_code | INTEGER | Unique AMFI scheme code for each mutual fund | fund_master.csv |
| scheme_name | TEXT | Name of the mutual fund scheme | fund_master.csv |
| fund_house | TEXT | Asset management company name | fund_master.csv |
| category | TEXT | Main category of the scheme | fund_master.csv |
| sub_category | TEXT | Sub-category of the scheme | fund_master.csv |
| risk_grade | TEXT | Risk level of the scheme | fund_master.csv |

## dim_date

| Column | Data Type | Business Meaning | Source |
|---|---|---|---|
| date_key | INTEGER | Date identifier in YYYYMMDD format | Generated |
| full_date | DATE | Actual calendar date | Generated |
| year | INTEGER | Year of the date | Generated |
| quarter | INTEGER | Quarter of the year | Generated |
| month | INTEGER | Month number | Generated |
| month_name | TEXT | Month name | Generated |
| day | INTEGER | Day of month | Generated |

## fact_nav

| Column | Data Type | Business Meaning | Source |
|---|---|---|---|
| nav_id | INTEGER | Unique NAV record ID | Generated |
| amfi_code | INTEGER | Mutual fund scheme code | nav_history.csv |
| date_key | INTEGER | Date key linked with dim_date | nav_history.csv |
| nav | REAL | Net Asset Value of the scheme | nav_history.csv |

## fact_transactions

| Column | Data Type | Business Meaning | Source |
|---|---|---|---|
| transaction_id | INTEGER | Unique transaction ID | investor_transactions.csv |
| amfi_code | INTEGER | Mutual fund scheme code | investor_transactions.csv |
| date_key | INTEGER | Transaction date key | investor_transactions.csv |
| investor_id | TEXT | Unique investor ID | investor_transactions.csv |
| transaction_type | TEXT | SIP, Lumpsum, or Redemption | investor_transactions.csv |
| amount | REAL | Transaction amount | investor_transactions.csv |
| state | TEXT | Investor state | investor_transactions.csv |
| kyc_status | TEXT | KYC verification status | investor_transactions.csv |

## fact_performance

| Column | Data Type | Business Meaning | Source |
|---|---|---|---|
| performance_id | INTEGER | Unique performance record ID | Generated |
| amfi_code | INTEGER | Mutual fund scheme code | scheme_performance.csv |
| return_1m | REAL | One-month return percentage | scheme_performance.csv |
| return_3m | REAL | Three-month return percentage | scheme_performance.csv |
| return_6m | REAL | Six-month return percentage | scheme_performance.csv |
| return_1y | REAL | One-year return percentage | scheme_performance.csv |
| return_3y | REAL | Three-year return percentage | scheme_performance.csv |
| return_5y | REAL | Five-year return percentage | scheme_performance.csv |
| expense_ratio | REAL | Expense ratio percentage | scheme_performance.csv |

## fact_aum

| Column | Data Type | Business Meaning | Source |
|---|---|---|---|
| aum_id | INTEGER | Unique AUM record ID | Generated |
| amfi_code | INTEGER | Mutual fund scheme code | AUM dataset |
| date_key | INTEGER | Date key linked with dim_date | AUM dataset |
| aum | REAL | Assets under management | AUM dataset |