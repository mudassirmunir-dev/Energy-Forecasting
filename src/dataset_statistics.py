
# Name: Mudassir Munir
# Roll No: PSEB-2026-010784
# Date: 2026-11-18

from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "raw" / "bdg2"


def get_dataset_statistics(name, file_path):
    print("\n" + "=" * 55)
    print(f"{name.upper()} DATASET STATISTICS")
    print("=" * 55)

    # Count columns without loading the entire dataset
    columns = pd.read_csv(file_path, nrows=0).columns

    # Count actual data rows
    row_count = sum(
        1 for _ in open(file_path, encoding="utf-8")
    ) - 1

    print("Total rows:", row_count)
    print("Total columns:", len(columns))
    print("Total cells:", row_count * len(columns))


def main():
    datasets = {
        "Electricity": DATA_DIR / "electricity.csv",
        "Weather": DATA_DIR / "weather.csv",
        "Metadata": DATA_DIR / "metadata" / "metadata.csv",
    }

    for name, path in datasets.items():
        get_dataset_statistics(name, path)


if __name__ == "__main__":
    main()
