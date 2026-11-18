
# Name: Mudassir Munir
# Roll No: PSEB-2026-010784
# Date: 2026-11-18

from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "raw" / "bdg2"

FILES = {
    "Electricity": DATA_DIR / "electricity.csv",
    "Weather": DATA_DIR / "weather.csv",
    "Metadata": DATA_DIR / "metadata" / "metadata.csv",
}


def inspect_dataset(name, file_path):
    print("\n" + "=" * 60)
    print(f"DATASET: {name.upper()}")
    print("=" * 60)

    if not file_path.exists():
        print(f"File not found: {file_path}")
        return

    # Read only five rows
    df = pd.read_csv(file_path, nrows=5)

    print("File size:", round(file_path.stat().st_size / (1024 ** 2), 2), "MB")
    print("Columns:", len(df.columns))

    print("\nFirst 10 column names:")
    print(df.columns[:10].tolist())

    print("\nData types of first 10 columns:")
    print(df.dtypes.head(10))

    print("\nFirst 5 rows and first 8 columns:")
    print(df.iloc[:, :8].to_string(index=False))


def main():
    for name, file_path in FILES.items():
        inspect_dataset(name, file_path)


if __name__ == "__main__":
    main()
