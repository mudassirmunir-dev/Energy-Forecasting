
# Name: Mudassir Munir
# Roll No: PSEB-2026-010784
# Date: 2026-11-18

from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent

FILE_PATH = (
    BASE_DIR
    / "data"
    / "cleaned"
    / "electricity.csv"
)


def analyze_buildings():
    missing_counts = None
    total_rows = 0

    for chunk in pd.read_csv(FILE_PATH, chunksize=2000):

        building_data = chunk.drop(columns=["timestamp"])

        chunk_missing = building_data.isna().sum()

        if missing_counts is None:
            missing_counts = chunk_missing
        else:
            missing_counts += chunk_missing

        total_rows += len(chunk)

    missing_percentage = (
        missing_counts / total_rows
    ) * 100

    report = pd.DataFrame({
        "Missing Values": missing_counts,
        "Missing Percentage": missing_percentage
    })

    report = report.sort_values(
        by="Missing Percentage",
        ascending=False
    )

    # Categorize buildings based on missing percentages
    reliable = report["Missing Percentage"] < 20

    moderate = (
        (report["Missing Percentage"] >= 20)
        & (report["Missing Percentage"] <= 50)
    )

    high_missing = report["Missing Percentage"] > 50

    print("\nBUILDING QUALITY CATEGORIES")
    print("=" * 60)

    print("Less than 20% missing:", reliable.sum())
    print("20% to 50% missing:", moderate.sum())
    print("More than 50% missing:", high_missing.sum())

    # Save the complete report
    output_path = BASE_DIR / "outputs" / "reports" / "building_missing_report.csv"

    output_path.parent.mkdir(parents=True, exist_ok=True)

    report.to_csv(output_path)

    print("\nReport saved:", output_path)

    print("\nBUILDING MISSING-VALUE ANALYSIS")
    print("=" * 60)

    print("\nBuildings with highest missing percentages:")
    print(report.head(20).round(2).to_string())

    print("\nBuildings with less than 20% missing:")
    print((report["Missing Percentage"] < 20).sum())

    print("\nBuildings with more than 50% missing:")
    print((report["Missing Percentage"] > 50).sum())


if __name__ == "__main__":
    analyze_buildings()
