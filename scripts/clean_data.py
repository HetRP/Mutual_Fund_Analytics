import pandas as pd
from pathlib import Path

raw = Path("data/raw")
processed = Path("data/processed")
processed.mkdir(parents=True, exist_ok=True)


def clean_nav_history():
    df = pd.read_csv(raw / "02_nav_history.csv")

    print("Cleaning 02_nav_history.csv")

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["nav"] = pd.to_numeric(df["nav"], errors="coerce")

    df = df.drop_duplicates()
    df = df.sort_values(["amfi_code", "date"])

    df["nav"] = df.groupby("amfi_code")["nav"].ffill()

    anomalies = df[(df["nav"] <= 0) | (df["nav"].isna())]
    print("NAV anomalies:", anomalies.shape[0])

    df = df[df["nav"] > 0]

    df.to_csv(processed / "nav_history_cleaned.csv", index=False)
    print("Saved nav_history_cleaned.csv")


def clean_investor_transactions():
    df = pd.read_csv(raw / "08_investor_transactions.csv")

    print("Cleaning 08_investor_transactions.csv")

    df["transaction_date"] = pd.to_datetime(df["transaction_date"], errors="coerce")
    df["amount_inr"] = pd.to_numeric(df["amount_inr"], errors="coerce")

    df["transaction_type"] = df["transaction_type"].str.strip().str.lower()

    transaction_map = {
        "sip": "SIP",
        "systematic investment plan": "SIP",
        "lumpsum": "Lumpsum",
        "lump sum": "Lumpsum",
        "redemption": "Redemption",
        "redeem": "Redemption"
    }

    df["transaction_type"] = df["transaction_type"].map(transaction_map)

    valid_kyc = ["Verified", "Pending", "Rejected"]

    df["kyc_status"] = df["kyc_status"].str.strip().str.title()

    invalid_amount = df[df["amount_inr"] <= 0]
    invalid_kyc = df[~df["kyc_status"].isin(valid_kyc)]
    invalid_type = df[df["transaction_type"].isna()]

    print("Invalid amounts:", invalid_amount.shape[0])
    print("Invalid KYC values:", invalid_kyc.shape[0])
    print("Invalid transaction types:", invalid_type.shape[0])

    df = df[df["amount_inr"] > 0]
    df = df[df["kyc_status"].isin(valid_kyc)]
    df = df[df["transaction_type"].notna()]

    df.to_csv(processed / "investor_transactions_cleaned.csv", index=False)
    print("Saved investor_transactions_cleaned.csv")


def clean_scheme_performance():
    df = pd.read_csv(raw / "07_scheme_performance.csv")

    print("Cleaning 07_scheme_performance.csv")

    numeric_cols = [
        "return_1m",
        "return_3m",
        "return_6m",
        "return_1y",
        "return_3y",
        "return_5y",
        "expense_ratio"
    ]

    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    if "expense_ratio" in df.columns:
        expense_anomalies = df[
            (df["expense_ratio"] < 0.1) | 
            (df["expense_ratio"] > 2.5)
        ]

        print("Expense ratio anomalies:", expense_anomalies.shape[0])

    return_cols = [col for col in numeric_cols if "return" in col and col in df.columns]

    for col in return_cols:
        anomalies = df[(df[col] < -100) | (df[col] > 200)]
        print(f"{col} anomalies:", anomalies.shape[0])

    df.to_csv(processed / "scheme_performance_cleaned.csv", index=False)
    print("Saved scheme_performance_cleaned.csv")


def copy_other_csvs():
    cleaned_files = {
        "02_nav_history.csv",
        "08_investor_transactions.csv",
        "07_scheme_performance.csv"
    }

    for file in raw.glob("*.csv"):
        if file.name not in cleaned_files:
            df = pd.read_csv(file)
            output_name = file.stem + "_cleaned.csv"
            df.to_csv(processed / output_name, index=False)

    print("Other CSVs copied to processed folder")


clean_nav_history()
clean_investor_transactions()
clean_scheme_performance()
copy_other_csvs()

print("Day 2 cleaning completed.")