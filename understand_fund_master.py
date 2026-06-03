import pandas as pd

fund_master = pd.read_csv("data/raw/01_fund_master.csv")

print("Columns in fund_master:")
print(fund_master.columns)

print("\nFirst 5 rows:")
print(fund_master.head())

print("\nUnique Fund Houses:")
print(fund_master["fund_house"].unique())

print("\nUnique Categories:")
print(fund_master["category"].unique())

print("\nUnique Sub-Categories:")
print(fund_master["sub_category"].unique())

print("\nUnique Risk Grades:")
print(fund_master["risk_category"].unique())

print("\nAMFI Scheme Code Sample:")
print(fund_master["amfi_code"].head(10))