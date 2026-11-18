
# Name: Mudassir Munir
# Roll No: PSEB-2026-010784
# Date: 2026-11-18

from pathlib import Path

import pandas as pd
import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parent.parent

ELECTRICITY_PATH = (
    PROJECT_ROOT / "data" / "cleaned" / "electricity_selected.csv"
)
WEATHER_PATH = (
    PROJECT_ROOT / "data" / "raw" / "bdg2" / "weather.csv"
)
METADATA_PATH = (
    PROJECT_ROOT / "outputs" / "reports"
    / "selected_building_metadata.csv"
)

REPORTS_DIR = PROJECT_ROOT / "outputs" / "reports"

BUILDING_ID = "Hog_lodging_Shonda"
SITE_ID = "Hog"


def load_candidate():
    print(f"Loading candidate: {BUILDING_ID}")

    electricity = pd.read_csv(
        ELECTRICITY_PATH,
        usecols=["timestamp", BUILDING_ID],
        parse_dates=["timestamp"]
    )

    electricity = electricity.rename(
        columns={BUILDING_ID: "consumption"}
    )

    return electricity


def analyze_readings(data):
    print("\n--- Electricity Reading Analysis ---")

    values = data["consumption"]

    print(f"Total readings: {len(data):,}")
    print(f"Missing readings: {values.isna().sum():,}")
    print(f"Zero readings: {(values == 0).sum():,}")
    print(f"Negative readings: {(values < 0).sum():,}")
    print(f"Unique readings: {values.nunique():,}")

    print("\nDescriptive statistics:")
    print(values.describe().round(3).to_string())

    print("\nFirst timestamp:", data["timestamp"].min())
    print("Last timestamp:", data["timestamp"].max())


def analyze_monthly_patterns(data):
    print("\n--- Monthly Consumption ---")

    data = data.copy()
    data["month"] = data["timestamp"].dt.to_period("M")

    monthly = data.groupby("month")["consumption"].agg(
        ["count", "mean", "median", "min", "max"]
    )

    monthly["mean"] = monthly["mean"].round(3)
    monthly["median"] = monthly["median"].round(3)

    print(monthly.to_string())

    monthly_path = REPORTS_DIR / "final_candidate_monthly_report.csv"
    monthly.to_csv(monthly_path)

    print(f"\nMonthly report saved: {monthly_path}")

    print("\n--- Same Month: 2016 vs 2017 ---")

    data["year"] = data["timestamp"].dt.year
    data["month_number"] = data["timestamp"].dt.month

    comparison = data.groupby(
        ["year", "month_number"]
    )["consumption"].mean().unstack("year")

    if 2016 in comparison.columns and 2017 in comparison.columns:
        comparison["percentage_change"] = (
            (comparison[2017] - comparison[2016])
            / comparison[2016].replace(0, np.nan)
        ) * 100

    print(comparison.round(2).to_string())

    comparison_path = (
        REPORTS_DIR / "final_candidate_year_comparison.csv"
    )
    comparison.to_csv(comparison_path)

    print(f"\nYear comparison saved: {comparison_path}")


def analyze_zero_periods(data):
    print("\n--- Zero Reading Periods ---")

    zero_data = data.loc[
        data["consumption"] == 0, "timestamp"
    ].sort_values()

    if zero_data.empty:
        print("No zero readings found.")
        return

    gaps = zero_data.diff().dt.total_seconds().div(3600)

    groups = gaps.ne(1).cumsum()

    periods = (
        zero_data.groupby(groups)
        .agg(["min", "max", "count"])
    )

    print(periods.to_string())


def check_weather_alignment(data):
    print("\n--- Weather Alignment ---")

    weather = pd.read_csv(
        WEATHER_PATH,
        usecols=["timestamp", "site_id"],
        parse_dates=["timestamp"]
    )

    site_weather = weather.loc[
        weather["site_id"] == SITE_ID
    ].copy()

    electricity_times = set(data["timestamp"])
    weather_times = set(site_weather["timestamp"])

    matched = len(electricity_times & weather_times)
    electricity_only = len(electricity_times - weather_times)

    percentage = matched / len(electricity_times) * 100

    print(f"Electricity timestamps: {len(electricity_times):,}")
    print(f"Weather timestamps: {len(weather_times):,}")
    print(f"Matched timestamps: {matched:,}")
    print(f"Electricity-only timestamps: {electricity_only:,}")
    print(f"Weather match percentage: {percentage:.2f}%")


def inspect_metadata():
    print("\n--- Building Metadata ---")

    metadata = pd.read_csv(METADATA_PATH)

    candidate = metadata.loc[
        metadata["building_id"] == BUILDING_ID
    ]

    if candidate.empty:
        print("Building metadata not found.")
        return

    columns = [
        "building_id",
        "site_id",
        "primaryspaceusage",
        "sub_primaryspaceusage",
        "sqm",
        "sqft",
        "yearbuilt",
        "numberoffloors",
        "occupants",
        "timezone"
    ]

    available = [col for col in columns if col in candidate.columns]

    print(candidate[available].to_string(index=False))


def main():
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    data = load_candidate()

    analyze_readings(data)
    analyze_monthly_patterns(data)
    analyze_zero_periods(data)
    check_weather_alignment(data)
    inspect_metadata()

    print("\nCandidate inspection completed.")


if __name__ == "__main__":
    main()
