import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine, text

processed = Path("data/processed")
db_path = "bluestock_mf.db"

engine = create_engine(f"sqlite:///{db_path}")


def create_date_dimension(dates):
    date_df = pd.DataFrame({"full_date": pd.to_datetime(dates).dropna().unique()})
    date_df["full_date"] = pd.to_datetime(date_df["full_date"])

    date_df["date_key"] = date_df["full_date"].dt.strftime("%Y%m%d").astype(int)
    date_df["year"] = date_df["full_date"].dt.year
    date_df["quarter"] = date_df["full_date"].dt.quarter
    date_df["month"] = date_df["full_date"].dt.month
    date_df["month_name"] = date_df["full_date"].dt.month_name()
    date_df["day"] = date_df["full_date"].dt.day

    return date_df


with engine.begin() as conn:
    with open("sql/schema.sql", "r") as file:
        schema_sql = file.read()

    for statement in schema_sql.split(";"):
        if statement.strip():
            conn.execute(text(statement))


print("Schema created successfully.")


fund_master = pd.read_csv(processed / "01_fund_master_cleaned.csv")
nav_history = pd.read_csv(processed / "02_nav_history_cleaned.csv")
transactions = pd.read_csv(processed / "08_investor_transactions_cleaned.csv")
performance = pd.read_csv(processed / "07_scheme_performance_cleaned.csv")

nav_history["date"] = pd.to_datetime(nav_history["date"])
transactions["transaction_date"] = pd.to_datetime(transactions["transaction_date"])

all_dates = pd.concat([
    nav_history["date"],
    transactions["transaction_date"]
])

dim_date = create_date_dimension(all_dates)

dim_fund = fund_master[[
    "amfi_code",
    "scheme_name",
    "fund_house",
    "category",
    "sub_category",
    "risk_category"
]].drop_duplicates()

fact_nav = nav_history.copy()
fact_nav["date_key"] = fact_nav["date"].dt.strftime("%Y%m%d").astype(int)
fact_nav = fact_nav[["amfi_code", "date_key", "nav"]]

fact_transactions = transactions.copy()
fact_transactions["date_key"] = fact_transactions["transaction_date"].dt.strftime("%Y%m%d").astype(int)
# fact_transactions["transaction_id"] = range(
#     1,
#     len(fact_transactions) + 1
# )
fact_transactions = fact_transactions[[
    # "transaction_id",
    "amfi_code",
    "date_key",
    "investor_id",
    "transaction_type",
    "amount_inr",
    "state",
    "kyc_status"
]]

fact_performance = performance[[
    "amfi_code",
    "return_1yr_pct",
    "return_3yr_pct",
    "return_5yr_pct",
    "expense_ratio_pct"
]]

with engine.begin() as conn:
    dim_fund.to_sql("dim_fund", conn, if_exists="append", index=False)
    dim_date.to_sql("dim_date", conn, if_exists="append", index=False)
    fact_nav.to_sql("fact_nav", conn, if_exists="append", index=False)
    fact_transactions.to_sql("fact_transactions", conn, if_exists="append", index=False)
    fact_performance.to_sql("fact_performance", conn, if_exists="append", index=False)

print("Data loaded into SQLite successfully.")

with engine.begin() as conn:
    tables = [
        "dim_fund",
        "dim_date",
        "fact_nav",
        "fact_transactions",
        "fact_performance"
    ]

    for table in tables:
        result = conn.execute(text(f"SELECT COUNT(*) FROM {table}"))
        count = result.scalar()
        print(f"{table}: {count} rows")

print("This process completed...")