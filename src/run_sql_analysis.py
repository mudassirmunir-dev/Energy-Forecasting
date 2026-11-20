
# Name: Mudassir Munir
# Roll No: PSEB-2026-010784
# Date: 2026-11-18

from pathlib import Path
import sqlite3

import pandas as pd


ROOT = Path(__file__).resolve().parent.parent

DATABASE_PATH = ROOT / "data" / "cleaned" / "energy_analysis.db"
SQL_PATH = ROOT / "sql" / "building_usage_analysis.sql"
OUTPUT_PATH = ROOT / "outputs" / "reports" / "sql_building_usage_analysis.csv"


def main():
    """Execute SQL analysis, validate the join, and save its results."""

    if not DATABASE_PATH.exists():
        raise FileNotFoundError(f"Database not found: {DATABASE_PATH}")

    if not SQL_PATH.exists():
        raise FileNotFoundError(f"SQL query not found: {SQL_PATH}")

    query = SQL_PATH.read_text(encoding="utf-8")

    with sqlite3.connect(DATABASE_PATH) as connection:
        energy_count = pd.read_sql_query(
            "SELECT COUNT(*) AS total FROM building_energy_summary",
            connection,
        ).iloc[0]["total"]

        metadata_count = pd.read_sql_query(
            "SELECT COUNT(*) AS total FROM building_metadata",
            connection,
        ).iloc[0]["total"]

        matched_count = pd.read_sql_query(
            """
            SELECT COUNT(*) AS total
            FROM building_energy_summary AS e
            INNER JOIN building_metadata AS m
                ON e.building_id = m.building_id
            """,
            connection,
        ).iloc[0]["total"]

        results = pd.read_sql_query(query, connection)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    results.to_csv(OUTPUT_PATH, index=False)

    print("\n========== SQLITE DATABASE VALIDATION ==========")
    print(f"Energy summary records: {energy_count}")
    print(f"Metadata records: {metadata_count}")
    print(f"Matched building records: {matched_count}")

    print("\n========== SQL QUERY RESULTS ==========")
    print(results.to_string(index=False))

    print("\n========== OUTPUT ==========")
    print(f"Saved results to: {OUTPUT_PATH}")
    print(f"Number of usage categories: {len(results)}")

    if results.empty:
        raise RuntimeError("SQL query returned no results.")

    if matched_count == 0:
        raise RuntimeError("The building metadata join returned no matches.")

    print("\nSQLite analysis completed successfully.")


if __name__ == "__main__":
    main()
