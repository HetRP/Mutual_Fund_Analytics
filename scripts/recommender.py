import pandas as pd
from pathlib import Path

processed = Path("data/processed")

performance = pd.read_csv(processed / "07_scheme_performance_cleaned.csv")

def recommend_funds(risk_appetite):
    risk_map = {
        "Low": ["Low", "Moderately Low"],
        "Moderate": ["Moderate"],
        "High": ["High", "Very High"]
    }

    allowed_risks = risk_map.get(risk_appetite)

    if allowed_risks is None:
        print("Invalid risk appetite. Choose Low, Moderate, or High.")
        return

    recommendations = performance[
        performance["risk_grade"].isin(allowed_risks)
    ].copy()

    recommendations = recommendations.sort_values(
        "sharpe_ratio",
        ascending=False
    ).head(3)

    print("\nTop 3 Recommended Funds")
    print("-" * 80)

    print(
        recommendations[[
            "scheme_name",
            "fund_house",
            "category",
            "risk_grade",
            "return_3yr_pct",
            "sharpe_ratio",
            "expense_ratio_pct",
            "aum_crore"
        ]]
    )


if __name__ == "__main__":
    risk = input("Enter risk appetite (Low / Moderate / High): ")
    recommend_funds(risk)