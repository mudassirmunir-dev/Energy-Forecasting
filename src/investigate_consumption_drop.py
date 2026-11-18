
# Name: Mudassir Munir
# Roll No: PSEB-2026-010784
# Date: 2026-11-18

"""
Investigate the unusual electricity consumption drop
between April and August 2017 for Robin_office_Wai.
"""

from pathlib import Path

import pandas as pd


# --------------------------------------------------
# 1. Configuration
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "cleaned"
    / "electricity_selected.csv"
)

REPORTS_DIR = PROJECT_ROOT / "outputs" / "reports"

BUILDING_ID = "Robin_office_Wai"

REPORTS_DIR.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# 2. Load data
# --------------------------------------------------

def load_data():
    print("Loading electricity data...")

    df = pd.read_csv(
        DATA_PATH,
        usecols=["timestamp", BUILDING_ID],
        parse_dates=["timestamp"]
    )

    df = df.rename(
        columns={BUILDING_ID: "electricity"}
    )

    df["year"] = df["timestamp"].dt.year
    df["month"] = df["timestamp"].dt.month

    print(f"Total records: {len(df):,}")

    return df


# --------------------------------------------------
# 3. Monthly consumption investigation
# --------------------------------------------------

def analyze_monthly_consumption(df):
    print("\nAnalyzing monthly consumption...")

    monthly = (
        df.groupby(["year", "month"])["electricity"]
        .agg(
            total_readings="count",
            mean="mean",
            median="median",
            minimum="min",
            maximum="max",
            standard_deviation="std",
            zero_readings=lambda x: (x == 0).sum(),
            nonzero_mean=lambda x: x[x > 0].mean(),
            nonzero_readings=lambda x: (x > 0).sum()
        )
        .reset_index()
    )

    monthly["zero_percentage"] = (
        monthly["zero_readings"]
        / monthly["total_readings"]
        * 100
    )

    monthly["month_label"] = (
        monthly["year"].astype(str)
        + "-"
        + monthly["month"].astype(str).str.zfill(2)
    )

    output_path = (
        REPORTS_DIR / "consumption_drop_investigation.csv"
    )

    monthly.to_csv(output_path, index=False)

    print("\nMonthly investigation results:")

    columns = [
        "month_label",
        "mean",
        "median",
        "minimum",
        "maximum",
        "zero_readings",
        "zero_percentage",
        "nonzero_mean"
    ]

    print(
        monthly[columns]
        .round(2)
        .to_string(index=False)
    )

    print(f"\nReport saved: {output_path}")

    return monthly


# --------------------------------------------------
# 4. Compare 2016 and 2017
# --------------------------------------------------

def compare_years(monthly):
    print("\nComparing the same months across 2016 and 2017...")

    comparison = monthly.pivot(
        index="month",
        columns="year",
        values="mean"
    )

    comparison = comparison.rename(
        columns={
            2016: "mean_2016",
            2017: "mean_2017"
        }
    )

    comparison["percentage_change"] = (
        (
            comparison["mean_2017"]
            - comparison["mean_2016"]
        )
        / comparison["mean_2016"]
    ) * 100

    print("\nYear-to-year monthly comparison:")

    print(comparison.round(2).to_string())

    output_path = (
        REPORTS_DIR / "yearly_monthly_comparison.csv"
    )

    comparison.to_csv(output_path)

    print(f"\nComparison saved: {output_path}")


# --------------------------------------------------
# 5. Inspect April to August 2017
# --------------------------------------------------

def inspect_unusual_period(df):
    print("\nInspecting April-August 2017...")

    unusual_period = df[
        (df["timestamp"] >= "2017-04-01")
        & (df["timestamp"] < "2017-09-01")
    ].copy()

    print(f"Total readings: {len(unusual_period):,}")

    print(
        f"Zero readings: "
        f"{(unusual_period['electricity'] == 0).sum()}"
    )

    print(
        f"Missing readings: "
        f"{unusual_period['electricity'].isna().sum()}"
    )

    print(
        f"Minimum reading: "
        f"{unusual_period['electricity'].min():.2f}"
    )

    print(
        f"Maximum reading: "
        f"{unusual_period['electricity'].max():.2f}"
    )

    print(
        f"Median reading: "
        f"{unusual_period['electricity'].median():.2f}"
    )

    print(
        f"Average reading: "
        f"{unusual_period['electricity'].mean():.2f}"
    )

    print(
        f"Average excluding zeros: "
        f"{unusual_period.loc[unusual_period['electricity'] > 0, 'electricity'].mean():.2f}"
    )


# --------------------------------------------------
# 6. Main execution
# --------------------------------------------------

def main():
    df = load_data()

    monthly = analyze_monthly_consumption(df)

    compare_years(monthly)

    inspect_unusual_period(df)

    print("\n" + "=" * 55)
    print("CONSUMPTION DROP INVESTIGATION COMPLETED")
    print("=" * 55)


if __name__ == "__main__":
    main()
