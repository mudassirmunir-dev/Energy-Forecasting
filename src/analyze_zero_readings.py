
# Name: Mudassir Munir
# Roll No: PSEB-2026-010784
# Date: 2026-11-18

import pandas as pd
from pathlib import Path

# --------------------------------------------------
# PROJECT PATHS
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

ELECTRICITY_FILE = (
    BASE_DIR / "data" / "cleaned"
    / "electricity_selected.csv"
)

OUTPUT_DIR = BASE_DIR / "outputs" / "reports"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

BUILDING_ID = "Robin_office_Wai"


# --------------------------------------------------
# ANALYZE ZERO READINGS
# --------------------------------------------------

def analyze_zero_readings():

    print("Loading electricity data...")

    df = pd.read_csv(
        ELECTRICITY_FILE,
        usecols=["timestamp", BUILDING_ID],
        parse_dates=["timestamp"]
    )

    df = df.sort_values("timestamp").reset_index(drop=True)

    # --------------------------------------------------
    # FIND ZERO READINGS
    # --------------------------------------------------

    zero_rows = df[df[BUILDING_ID] == 0].copy()

    print("\n1. ZERO READING SUMMARY")
    print("=" * 50)

    print(f"Total electricity records: {len(df)}")
    print(f"Zero readings: {len(zero_rows)}")
    print(
        f"Zero reading percentage: "
        f"{len(zero_rows) / len(df) * 100:.4f}%"
    )

    # --------------------------------------------------
    # DISPLAY ZERO TIMESTAMPS
    # --------------------------------------------------

    print("\n2. ZERO READING TIMESTAMPS")
    print("=" * 50)

    if zero_rows.empty:
        print("No zero readings found.")
    else:
        print(
            zero_rows[["timestamp", BUILDING_ID]]
            .to_string(index=False)
        )

    # --------------------------------------------------
    # FIND CONSECUTIVE ZERO PERIODS
    # --------------------------------------------------

    print("\n3. CONSECUTIVE ZERO PERIODS")
    print("=" * 50)

    is_zero = df[BUILDING_ID].eq(0)

    group_ids = (~is_zero).cumsum()

    zero_periods = (
        df[is_zero]
        .groupby(group_ids[is_zero])
        .agg(
            start_timestamp=("timestamp", "min"),
            end_timestamp=("timestamp", "max"),
            zero_hours=("timestamp", "count")
        )
        .reset_index(drop=True)
    )

    if zero_periods.empty:
        print("No consecutive zero periods found.")
    else:
        print(zero_periods.to_string(index=False))

    # --------------------------------------------------
    # SAVE REPORTS
    # --------------------------------------------------

    zero_rows.to_csv(
        OUTPUT_DIR / "zero_readings_report.csv",
        index=False
    )

    zero_periods.to_csv(
        OUTPUT_DIR / "zero_periods_report.csv",
        index=False
    )

    print("\n4. REPORTS SAVED")
    print("=" * 50)

    print("outputs/reports/zero_readings_report.csv")
    print("outputs/reports/zero_periods_report.csv")

    print("\nZero reading analysis completed!")


# --------------------------------------------------
# MAIN
# --------------------------------------------------

if __name__ == "__main__":
    analyze_zero_readings()
