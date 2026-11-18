
# Name: Mudassir Munir
# Roll No: PSEB-2026-010784
# Date: 2026-11-18

import pandas as pd
from pathlib import Path

# --------------------------------------------------
# PROJECT PATHS
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "data" / "cleaned" / "electricity_selected.csv"
REPORT_FILE = BASE_DIR / "outputs" / "reports" / "selected_missing_report.csv"

CHUNK_SIZE = 2000


# --------------------------------------------------
# ANALYZE MISSING VALUES
# --------------------------------------------------

def analyze_missing_values():

    print("Analyzing selected electricity dataset...")

    missing_counts = None
    total_rows = 0

    for chunk in pd.read_csv(INPUT_FILE, chunksize=CHUNK_SIZE):

        # Count missing values in each column
        chunk_missing = chunk.isna().sum()

        if missing_counts is None:
            missing_counts = chunk_missing
        else:
            missing_counts += chunk_missing

        total_rows += len(chunk)

        print(f"Analyzed {total_rows} rows")

    # Calculate missing percentages
    missing_percentages = (
        missing_counts / total_rows
    ) * 100

    report = pd.DataFrame({
        "Missing Values": missing_counts,
        "Missing Percentage": missing_percentages
    })

    # Sort by highest missing percentage
    report = report.sort_values(
        by="Missing Percentage",
        ascending=False
    )

    # Save report
    REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)
    report.to_csv(REPORT_FILE)

    print("\nMissing-value analysis completed!")

    print("\nTop 15 columns with missing values:")
    print(report.head(15).to_string())

    print("\nOverall statistics:")
    print(f"Total rows: {total_rows}")
    print(f"Total columns: {len(report)}")
    print(
        "Columns with missing values:",
        int((missing_counts > 0).sum())
    )
    print(
        "Columns without missing values:",
        int((missing_counts == 0).sum())
    )

    print(f"\nReport saved to: {REPORT_FILE}")


# --------------------------------------------------
# MAIN EXECUTION
# --------------------------------------------------

if __name__ == "__main__":
    analyze_missing_values()
