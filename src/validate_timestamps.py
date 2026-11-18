
# Name: Mudassir Munir
# Roll No: PSEB-2026-010784
# Date: 2026-11-18

import pandas as pd
from pathlib import Path

# --------------------------------------------------
# PROJECT PATHS
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    BASE_DIR
    / "data"
    / "cleaned"
    / "electricity_selected.csv"
)

REPORT_FILE = (
    BASE_DIR
    / "outputs"
    / "reports"
    / "timestamp_validation_report.csv"
)


# --------------------------------------------------
# VALIDATE TIMESTAMPS
# --------------------------------------------------

def validate_timestamps():

    print("Loading timestamps...")

    df = pd.read_csv(
        INPUT_FILE,
        usecols=["timestamp"],
        parse_dates=["timestamp"]
    )

    print(f"Total records: {len(df)}")

    # Check invalid timestamps
    invalid_count = int(df["timestamp"].isna().sum())

    # Sort timestamps chronologically
    timestamps = df["timestamp"].dropna().sort_values()

    # Check duplicate timestamps
    duplicate_count = int(timestamps.duplicated().sum())

    # Calculate differences between consecutive timestamps
    time_differences = timestamps.diff().dropna()

    expected_difference = pd.Timedelta(hours=1)

    # Count intervals that are not exactly one hour
    irregular_intervals = int(
        (time_differences != expected_difference).sum()
    )

    # Find missing hourly intervals
    missing_intervals = time_differences[
        time_differences > expected_difference
    ]

    # Find intervals shorter than one hour
    shorter_intervals = time_differences[
        time_differences < expected_difference
    ]

    # Prepare report
    results = {
        "Total Records": len(df),
        "Invalid Timestamps": invalid_count,
        "Duplicate Timestamps": duplicate_count,
        "Irregular Intervals": irregular_intervals,
        "Missing Hourly Intervals": len(missing_intervals),
        "Shorter Intervals": len(shorter_intervals),
        "First Timestamp": str(timestamps.min()),
        "Last Timestamp": str(timestamps.max()),
        "Expected Interval": "1 hour"
    }

    report = pd.DataFrame(
        [results]
    )

    REPORT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    report.to_csv(
        REPORT_FILE,
        index=False
    )

    # Display results
    print("\nTIMESTAMP VALIDATION RESULTS")
    print("--------------------------------")

    for key, value in results.items():
        print(f"{key}: {value}")

    print("\nFirst 10 timestamp differences:")
    print(time_differences.head(10))

    print("\nTimestamp validation completed!")
    print(f"Report saved to: {REPORT_FILE}")


# --------------------------------------------------
# MAIN EXECUTION
# --------------------------------------------------

if __name__ == "__main__":
    validate_timestamps()
