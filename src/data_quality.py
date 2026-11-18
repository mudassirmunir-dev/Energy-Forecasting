
# Name: Mudassir Munir
# Roll No: PSEB-2026-010784
# Date: 2026-11-18

from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "raw" / "bdg2"


def analyze_data_quality(name, file_path):
    print("\n" + "=" * 60)
    print(f"{name.upper()} DATA QUALITY REPORT")
    print("=" * 60)

    missing_counts = None
    total_rows = 0
    duplicate_rows = 0

    # Process the dataset in smaller chunks
    for chunk in pd.read_csv(file_path, chunksize=5000):

        # Count missing values in each column
        chunk_missing = chunk.isnull().sum()

        if missing_counts is None:
            missing_counts = chunk_missing
        else:
            missing_counts += chunk_missing

        total_rows += len(chunk)

        # Count completely duplicated rows within each chunk
        duplicate_rows += chunk.duplicated().sum()

    # Calculate missing-value percentages
    missing_percentage = (missing_counts / total_rows) * 100

    report = pd.DataFrame({
        "Missing Values": missing_counts,
        "Missing Percentage": missing_percentage.round(2)
    })

    print("Total rows:", total_rows)
    print("Duplicate rows within chunks:", duplicate_rows)
    print("Completely empty columns:", (missing_counts == total_rows).sum())

    print("\nColumns with the most missing values:")
    print(report.sort_values(
        by="Missing Percentage",
        ascending=False
    ).head(15))


def main():
    datasets = {
        "Electricity": DATA_DIR / "electricity.csv",
        "Weather": DATA_DIR / "weather.csv",
        "Metadata": DATA_DIR / "metadata" / "metadata.csv",
    }

    for name, path in datasets.items():
        analyze_data_quality(name, path)


if __name__ == "__main__":
    main()
