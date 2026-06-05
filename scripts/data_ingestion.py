import pandas as pd
from pathlib import Path

raw = Path("data/raw")

csv_files_list = list(raw.glob("*.csv"))

for file in csv_files_list:
    print(f"\n\nFiles: {file.name}")
    df = pd.read_csv(file)

    print(f"\n Shape:\n {df.shape}")

    print(f"\n Head:\n {df.head()}")

    print(f"\n Missing Values:\n {df.isnull().sum()}")

    print(f"\n Duplicate Rows:\n {df.duplicated().sum}")

    print("\n Anomaly Notes:")

    if df.empty:
        print("\n -- Dataset is empty")

    if df.isnull().sum().sum() > 0:
        print("\n -- Missing values found")

    if df.duplicated().sum() > 0:
        print("\n -- Duplicate rows found")

    if df.shape[1] == 0:
        print("\n -- No columns found")

print("\nData Ingestion Completed")