
# Name: Mudassir Munir
# Roll No: PSEB-2026-010784
# Date: 2026-11-18

from pathlib import Path
import sqlite3

import pandas as pd


ROOT = Path(__file__).resolve().parent.parent

ELECTRICITY_PATH = ROOT / "data" / "cleaned" / "electricity_selected.csv"
METADATA_PATH = ROOT / "data" / "raw" / "bdg2" / "metadata" / "metadata.csv"

DATABASE_PATH = ROOT / "data" / "cleaned" / "energy_analysis.db"

CHUNK_SIZE = 1000


def calculate_building_summaries():
    """Calculate energy statistics for each building in chunks."""

    building_sums = None
    building_counts = None

    for chunk in pd.read_csv(ELECTRICITY_PATH, chunksize=CHUNK_SIZE):
        readings = chunk.drop(columns=["timestamp"])

        readings = readings.apply(pd.to_numeric, errors="coerce")

        chunk_sums = readings.sum()
        chunk_counts = readings.count()

        if building_sums is None:
            building_sums = chunk_sums
            building_counts = chunk_counts
        else:
            building_sums = building_sums.add(chunk_sums, fill_value=0)
            building_counts = building_counts.add(
                chunk_counts, fill_value=0
            )

    summary = pd.DataFrame({
        "building_id": building_sums.index,
        "total_consumption": building_sums.values,
        "reading_count": building_counts.values,
    })

    summary["average_consumption"] = (
        summary["total_consumption"] / summary["reading_count"]
    )

    return summary


def build_database():
    """Create SQLite tables and insert building summaries and metadata."""

    if not ELECTRICITY_PATH.exists():
        raise FileNotFoundError(ELECTRICITY_PATH)

    if not METADATA_PATH.exists():
        raise FileNotFoundError(METADATA_PATH)

    print("Calculating electricity summaries...")
    energy_summary = calculate_building_summaries()

    print("Loading building metadata...")
    metadata = pd.read_csv(METADATA_PATH)

    metadata = metadata[
        ["building_id", "site_id", "primaryspaceusage", "sqm"]
    ].copy()

    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(DATABASE_PATH) as connection:
        energy_summary.to_sql(
            "building_energy_summary",
            connection,
            if_exists="replace",
            index=False,
        )

        metadata.to_sql(
            "building_metadata",
            connection,
            if_exists="replace",
            index=False,
        )

        connection.execute("""
            CREATE INDEX IF NOT EXISTS
            idx_energy_building_id
            ON building_energy_summary(building_id)
        """)

        connection.execute("""
            CREATE INDEX IF NOT EXISTS
            idx_metadata_building_id
            ON building_metadata(building_id)
        """)

    print("\nSQLite database created successfully.")
    print(f"Database: {DATABASE_PATH}")
    print(f"Energy summary records: {len(energy_summary)}")
    print(f"Metadata records: {len(metadata)}")


if __name__ == "__main__":
    build_database()
