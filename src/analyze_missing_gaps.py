
# Name: Mudassir Munir
# Roll No: PSEB-2026-010784
# Date: 2026-11-18

import pandas as pd
from pathlib import Path

# --------------------------------------------------
# PROJECT PATHS
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_FILE = BASE_DIR / "data" / "cleaned" / "electricity_selected.csv"

MISSING_REPORT = (
    BASE_DIR
    / "outputs"
    / "reports"
    / "selected_missing_report.csv"
)

OUTPUT_FILE = (
    BASE_DIR
    / "outputs"
    / "reports"
    / "missing_gap_analysis.csv"
)

TOP_N = 20


# --------------------------------------------------
# ANALYZE MISSING GAPS
# --------------------------------------------------

def analyze_building_gaps(series):

    missing_mask = series.isna()

    missing_count = int(missing_mask.sum())

    if missing_count == 0:
        return {
            "Missing Readings": 0,
            "Missing Periods": 0,
            "Longest Gap (Hours)": 0,
            "Average Gap (Hours)": 0
        }

    # Identify the beginning of each missing period
    gap_starts = missing_mask & ~missing_mask.shift(
        fill_value=False
    )

    # Assign a unique group number to each continuous period
    groups = gap_starts.cumsum()

    # Calculate the length of each missing period
    gap_lengths = (
        missing_mask[missing_mask]
        .groupby(groups[missing_mask])
        .sum()
    )

    return {
        "Missing Readings": missing_count,
        "Missing Periods": len(gap_lengths),
        "Longest Gap (Hours)": int(gap_lengths.max()),
        "Average Gap (Hours)": round(
            gap_lengths.mean(), 2
        )
    }


# --------------------------------------------------
# MAIN ANALYSIS
# --------------------------------------------------

def analyze_missing_gaps():

    print("Loading missing-value report...")

    report = pd.read_csv(
        MISSING_REPORT,
        index_col=0
    )

    # Select top 20 buildings with highest missing percentage
    top_buildings = report.head(TOP_N).index.tolist()

    print(f"Selected buildings for analysis: {len(top_buildings)}")

    print("\nLoading selected electricity readings...")

    # Load only required columns
    columns = ["timestamp"] + top_buildings

    df = pd.read_csv(
        DATA_FILE,
        usecols=columns,
        parse_dates=["timestamp"]
    )

    # Ensure chronological order
    df = df.sort_values("timestamp").reset_index(drop=True)

    results = []

    print("\nAnalyzing missing periods...")

    for building in top_buildings:

        gap_analysis = analyze_building_gaps(df[building])

        gap_analysis["Building ID"] = building

        results.append(gap_analysis)

        print(
            f"Analyzed: {building} | "
            f"Missing periods: {gap_analysis['Missing Periods']} | "
            f"Longest gap: {gap_analysis['Longest Gap (Hours)']} hours"
        )

    # Create results DataFrame
    results_df = pd.DataFrame(results)

    # Arrange columns
    results_df = results_df[
        [
            "Building ID",
            "Missing Readings",
            "Missing Periods",
            "Longest Gap (Hours)",
            "Average Gap (Hours)"
        ]
    ]

    # Save report
    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    results_df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print("\nMissing-gap analysis completed!")

    print("\nFinal Report:")
    print(results_df.to_string(index=False))

    print(f"\nReport saved to: {OUTPUT_FILE}")


# --------------------------------------------------
# EXECUTION
# --------------------------------------------------

if __name__ == "__main__":
    analyze_missing_gaps()
