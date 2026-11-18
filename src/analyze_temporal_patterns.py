
# Name: Mudassir Munir
# Roll No: PSEB-2026-010784
# Date: 2026-11-18

"""
Analyze hourly, daily, and monthly electricity consumption patterns
for the selected building: Robin_office_Wai.
"""

from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


# --------------------------------------------------
# 1. Project paths and configuration
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "cleaned"
    / "electricity_selected.csv"
)

FIGURES_DIR = PROJECT_ROOT / "outputs" / "figures"
REPORTS_DIR = PROJECT_ROOT / "outputs" / "reports"

BUILDING_ID = "Robin_office_Wai"

FIGURES_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# 2. Load selected building data
# --------------------------------------------------

def load_building_data():
    print("Loading selected building data...")

    df = pd.read_csv(
        DATA_PATH,
        usecols=["timestamp", BUILDING_ID],
        parse_dates=["timestamp"]
    )

    df = df.rename(
        columns={BUILDING_ID: "electricity"}
    )

    df = df.sort_values("timestamp").reset_index(drop=True)

    print(f"Total records: {len(df):,}")
    print(f"Missing readings: {df['electricity'].isna().sum()}")
    print(f"Date range: {df['timestamp'].min()} to {df['timestamp'].max()}")

    return df


# --------------------------------------------------
# 3. Analyze hourly consumption
# --------------------------------------------------

def analyze_hourly_patterns(df):
    print("\nAnalyzing hourly consumption...")

    df["hour"] = df["timestamp"].dt.hour

    hourly = (
        df.groupby("hour")["electricity"]
        .agg(["mean", "median", "min", "max", "count"])
        .reset_index()
    )

    hourly.to_csv(
        REPORTS_DIR / "hourly_consumption_report.csv",
        index=False
    )

    print("\nAverage consumption by hour:")
    print(hourly[["hour", "mean"]].round(2).to_string(index=False))

    plt.figure(figsize=(12, 6))

    plt.plot(
        hourly["hour"],
        hourly["mean"],
        marker="o"
    )

    plt.title("Average Electricity Consumption by Hour")
    plt.xlabel("Hour of Day")
    plt.ylabel("Average Electricity Reading")
    plt.xticks(range(0, 24))
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    plt.savefig(
        FIGURES_DIR / "hourly_consumption_pattern.png",
        dpi=300
    )

    plt.close()

    print("Saved hourly consumption chart.")


# --------------------------------------------------
# 4. Analyze daily consumption
# --------------------------------------------------

def analyze_daily_patterns(df):
    print("\nAnalyzing day-of-week consumption...")

    df["day_of_week"] = df["timestamp"].dt.day_name()

    day_order = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday"
    ]

    daily = (
        df.groupby("day_of_week")["electricity"]
        .agg(["mean", "median", "min", "max", "count"])
        .reindex(day_order)
        .reset_index()
    )

    daily.to_csv(
        REPORTS_DIR / "daily_consumption_report.csv",
        index=False
    )

    print("\nAverage consumption by day:")
    print(daily[["day_of_week", "mean"]].round(2).to_string(index=False))

    plt.figure(figsize=(12, 6))

    plt.bar(
        daily["day_of_week"],
        daily["mean"]
    )

    plt.title("Average Electricity Consumption by Day of Week")
    plt.xlabel("Day of Week")
    plt.ylabel("Average Electricity Reading")
    plt.xticks(rotation=30)
    plt.grid(axis="y", alpha=0.3)
    plt.tight_layout()

    plt.savefig(
        FIGURES_DIR / "daily_consumption_pattern.png",
        dpi=300
    )

    plt.close()

    print("Saved daily consumption chart.")


# --------------------------------------------------
# 5. Analyze monthly consumption
# --------------------------------------------------

def analyze_monthly_patterns(df):
    print("\nAnalyzing monthly consumption...")

    df["month"] = df["timestamp"].dt.to_period("M")

    monthly = (
        df.groupby("month")["electricity"]
        .agg(["mean", "median", "min", "max", "count"])
        .reset_index()
    )

    monthly["month"] = monthly["month"].astype(str)

    monthly.to_csv(
        REPORTS_DIR / "monthly_consumption_report.csv",
        index=False
    )

    print("\nAverage consumption by month:")
    print(monthly[["month", "mean"]].round(2).to_string(index=False))

    plt.figure(figsize=(15, 6))

    plt.plot(
        monthly["month"],
        monthly["mean"],
        marker="o"
    )

    plt.title("Average Monthly Electricity Consumption")
    plt.xlabel("Month")
    plt.ylabel("Average Electricity Reading")
    plt.xticks(rotation=60)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    plt.savefig(
        FIGURES_DIR / "monthly_consumption_pattern.png",
        dpi=300
    )

    plt.close()

    print("Saved monthly consumption chart.")


# --------------------------------------------------
# 6. Main execution
# --------------------------------------------------

def main():
    df = load_building_data()

    analyze_hourly_patterns(df)
    analyze_daily_patterns(df)
    analyze_monthly_patterns(df)

    print("\n" + "=" * 50)
    print("TEMPORAL PATTERN ANALYSIS COMPLETED")
    print("=" * 50)

    print("\nGenerated figures:")
    print("1. hourly_consumption_pattern.png")
    print("2. daily_consumption_pattern.png")
    print("3. monthly_consumption_pattern.png")

    print("\nGenerated reports:")
    print("1. hourly_consumption_report.csv")
    print("2. daily_consumption_report.csv")
    print("3. monthly_consumption_report.csv")


if __name__ == "__main__":
    main()
