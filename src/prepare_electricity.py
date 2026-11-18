
# Name: Mudassir Munir
# Roll No: PSEB-2026-010784
# Date: 2026-11-18

import pandas as pd
from pathlib import Path

# --------------------------------------------------
# PROJECT PATHS
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "data" / "cleaned" / "electricity.csv"
REPORT_FILE = BASE_DIR / "outputs" / "reports" / "building_missing_report.csv"
OUTPUT_FILE = BASE_DIR / "data" / "cleaned" / "electricity_selected.csv"

CHUNK_SIZE = 2000


# --------------------------------------------------
# STEP 1: PREPARE ELECTRICITY DATASET
# --------------------------------------------------

def prepare_electricity():

    print("Loading building missing-value report...")

    report = pd.read_csv(REPORT_FILE, index_col=0)

    # Select buildings with less than 20% missing readings
    selected_buildings = report.index[
        report["Missing Percentage"] < 20
    ].tolist()

    print(f"Selected buildings: {len(selected_buildings)}")

    total_rows = 0
    first_chunk = True

    print("\nPreparing electricity dataset...")

    for chunk in pd.read_csv(INPUT_FILE, chunksize=CHUNK_SIZE):

        # Keep timestamp and selected building columns
        columns_to_keep = ["timestamp"] + selected_buildings

        chunk = chunk[columns_to_keep].copy()

        # Convert timestamp to datetime
        chunk["timestamp"] = pd.to_datetime(
            chunk["timestamp"],
            errors="coerce"
        )

        # Save chunks into one CSV file
        chunk.to_csv(
            OUTPUT_FILE,
            mode="w" if first_chunk else "a",
            header=first_chunk,
            index=False
        )

        total_rows += len(chunk)
        first_chunk = False

        print(f"Processed {total_rows} rows")

    print("\nDataset preparation complete!")
    print(f"Total rows: {total_rows}")
    print(f"Building columns: {len(selected_buildings)}")
    print(f"Total columns: {len(selected_buildings) + 1}")
    print(f"Saved to: {OUTPUT_FILE}")


# --------------------------------------------------
# STEP 2: VERIFY PREPARED DATASET
# --------------------------------------------------

def verify_dataset():

    print("\nVerifying selected dataset...")

    # Read a small sample
    df = pd.read_csv(
        OUTPUT_FILE,
        nrows=5,
        parse_dates=["timestamp"]
    )

    print("\nFirst 5 rows (first 6 columns):")

    print(
        df.iloc[:, :6].to_string(index=False)
    )

    print("\nSample information:")
    print(f"Sample rows: {len(df)}")
    print(f"Total columns: {len(df.columns)}")
    print(f"Timestamp data type: {df['timestamp'].dtype}")

    # Count total rows without loading entire file
    total_rows = 0

    for chunk in pd.read_csv(
        OUTPUT_FILE,
        chunksize=CHUNK_SIZE
    ):
        total_rows += len(chunk)

    print(f"Total dataset rows: {total_rows}")

    print("\nVerification completed!")


# --------------------------------------------------
# MAIN EXECUTION
# --------------------------------------------------

if __name__ == "__main__":

    prepare_electricity()

    verify_dataset()
