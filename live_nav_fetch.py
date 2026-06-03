import pandas as pd
import requests
from pathlib import Path

raw = Path("data/raw")

schemes = {
    "HDFC_Top_100_Direct": "125497",
    "SBI_Bluechip": "119551",
    "ICICI_Bluechip": "120503",
    "Nippon_Large_Cap": "118632",
    "Axis_Bluechip": "119092",
    "Kotak_Bluechip": "120841"
}

all_nav_data = []

for scheme_name, scheme_code in schemes.items():
    url = f"https://api.mfapi.in/mf/{scheme_code}"
    print(f"\n{url}")

    print(f"Fetching NAV for {scheme_name}: ")

    response = requests.get(url)

    if response.status_code == 200:
        json_data = response.json()

        meta = json_data.get("meta", {})

        nav_data = json_data.get("data", [])

        df = pd.DataFrame(nav_data)

        df["scheme_code"] = scheme_code
        df["scheme_name"] = meta.get("scheme_name")
        df["fund_house"] = meta.get("fund_house")
        df["scheme_type"] = meta.get("scheme_type")
        df["scheme_category"] = meta.get("scheme_category")

        output_file = raw / f"{scheme_name}_live_nav.csv"
        df.to_csv(output_file, index=False)

        all_nav_data.append(df)

        print(f"Saved: {output_file}")

    else:
        print(F"Failed for {scheme_name}, Status Code: {response.status_code}")

if all_nav_data:
    combined_df = pd.concat(all_nav_data, ignore_index=True)
    combined_df.to_csv(raw / "all_live_nav.csv", index=False)
    print("\n\nCombined NAV saved as data/raw/all_live_nav.csv")