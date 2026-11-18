
# Name: Mudassir Munir
# Roll No: PSEB-2026-010784
# Date: 2026-11-18

from pathlib import Path
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent

RAW_FILE = BASE_DIR / "data" / "raw" / "bdg2" / "electricity.csv"

CLEANED_DIR = BASE_DIR / "data" / "cleaned"
CLEANED_FILE = CLEANED_DIR / "electricity.csv"

CHUNK_SIZE = 2000


def find_empty_columns(file_path):
    """Find columns that contain only missing values."""

    missing_counts = None
    total_rows = 0

    for chunk in pd.read_csv(file_path, chunksize=CHUNK_SIZE):

        chunk_missing = chunk.isna().sum()

        if missing_counts is None:
            missing_counts = chunk_missing
        else:
            missing_counts += chunk_missing

        total_rows += len(chunk)

    empty_columns = missing_counts[
        missing_counts == total_rows
    ].index.tolist()

    return empty_columns


def remove_empty_columns(file_path, output_path):
    """Remove completely empty columns and save the result."""

    empty_columns = find_empty_columns(file_path)

    print("Completely empty columns found:", empty_columns)

    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Read the original file again, this time without empty columns
    first_chunk = True

    for chunk in pd.read_csv(file_path, chunksize=CHUNK_SIZE):

        chunk = chunk.drop(columns=empty_columns)

        chunk.to_csv(
            output_path,
            mode="w" if first_chunk else "a",
            header=first_chunk,
            index=False
        )

        first_chunk = False

    print("\nCleaning completed!")
    print("Removed columns:", len(empty_columns))
    print("Saved cleaned file:", output_path)


def main():
    remove_empty_columns(RAW_FILE, CLEANED_FILE)


if __name__ == "__main__":
    main()
