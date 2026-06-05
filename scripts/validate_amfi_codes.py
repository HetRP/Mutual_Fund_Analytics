import pandas as pd

fund_master = pd.read_csv("data/raw/01_fund_master.csv")
nav_history = pd.read_csv("data/raw/02_nav_history.csv")

fund_master["amfi_code"] = fund_master["amfi_code"].astype(str)
nav_history["amfi_code"] = nav_history["amfi_code"].astype(str)

fund_codes = set(fund_master["amfi_code"])
nav_codes = set(nav_history["amfi_code"])

missing_in_nav = fund_codes - nav_codes
extra_in_nav = nav_codes - fund_codes

print("Data Quality Summary: ")

print(f"\nTotal scheme codes in fund_master: {len(fund_codes)}")
print(f"\nTotal scheme code in nav_hisory: {len(nav_codes)}")

print(f"\nScheme codes in fund_master but missing in nav_history: {len(missing_in_nav)}")
print(f"\nScheme codes in nav_history but missing in fund_master: {len(extra_in_nav)}")

if missing_in_nav:
    print("\nMissing codes:")
    print(list(missing_in_nav)[:20])

if extra_in_nav:
    print("\nExtra codes:")
    print(list(extra_in_nav)[:20])

if len(missing_in_nav) == 0:
    print("\nAll scheme codes from fund_master are available in nav_history.")
else:
    print("\nSome scheme codes from fund_master are missing in nav_history.")

if len(extra_in_nav) > 0:
    print("\nnav_history contains some extra scheme codes not found in fund_master.")