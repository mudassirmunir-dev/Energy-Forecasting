
# Name: Mudassir Munir
# Roll No: PSEB-2026-010784
# Date: 2026-11-18

import pandas as pd
from pathlib import Path

# --------------------------------------------------
# PROJECT PATHS
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

METADATA_FILE = (
    BASE_DIR / "data" / "raw" / "bdg2"
    / "metadata" / "metadata.csv"
)

ELECTRICITY_REPORT = (
    BASE_DIR / "outputs" / "reports"
    / "selected_missing_report.csv"
)

OUTPUT_DIR = BASE_DIR / "outputs" / "reports"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# INSPECT METADATA
# --------------------------------------------------

def inspect_metadata():

    print("Loading building metadata...")

    metadata = pd.read_csv(METADATA_FILE)

    print("\n1. DATASET INFORMATION")
    print("------------------------------")
    print(f"Rows: {metadata.shape[0]}")
    print(f"Columns: {metadata.shape[1]}")

    print("\nColumns:")
    print(metadata.columns.tolist())

    # --------------------------------------------------
    # MISSING VALUE ANALYSIS
    # --------------------------------------------------

    print("\n2. MISSING VALUE ANALYSIS")
    print("------------------------------")

    missing_report = pd.DataFrame({
        "Missing Values": metadata.isna().sum(),
        "Missing Percentage": metadata.isna().mean() * 100
    })

    missing_report = missing_report.sort_values(
        "Missing Percentage",
        ascending=False
    )

    print(missing_report.to_string())

    missing_report.to_csv(
        OUTPUT_DIR / "metadata_missing_report.csv"
    )

    # --------------------------------------------------
    # BUILDING USAGE DISTRIBUTION
    # --------------------------------------------------

    print("\n3. PRIMARY SPACE USAGE")
    print("------------------------------")

    usage_counts = (
        metadata["primaryspaceusage"]
        .fillna("Unknown")
        .value_counts()
    )

    print(usage_counts.to_string())

    usage_counts.to_csv(
        OUTPUT_DIR / "building_usage_report.csv",
        header=["Building Count"]
    )

    # --------------------------------------------------
    # MATCH ELECTRICITY BUILDINGS WITH METADATA
    # --------------------------------------------------

    print("\n4. BUILDING ID MATCHING")
    print("------------------------------")

    electricity_report = pd.read_csv(
        ELECTRICITY_REPORT,
        index_col=0
    )

    # Remove timestamp because it is not a building ID.
    selected_buildings = set(
        electricity_report.index.astype(str)
    )

    selected_buildings.discard("timestamp")

    metadata["building_id"] = (
        metadata["building_id"].astype(str)
    )

    metadata_buildings = set(metadata["building_id"])

    matched_buildings = (
        selected_buildings & metadata_buildings
    )

    unmatched_buildings = (
        selected_buildings - metadata_buildings
    )

    print(
        f"Selected electricity buildings: "
        f"{len(selected_buildings)}"
    )

    print(
        f"Buildings matched with metadata: "
        f"{len(matched_buildings)}"
    )

    print(
        f"Unmatched building IDs: "
        f"{len(unmatched_buildings)}"
    )

    if unmatched_buildings:
        print("\nUnmatched IDs:")
        for building_id in sorted(unmatched_buildings):
            print(building_id)

    # --------------------------------------------------
    # SAVE MATCHED METADATA
    # --------------------------------------------------

    matched_metadata = metadata[
        metadata["building_id"].isin(matched_buildings)
    ].copy()

    matched_metadata.to_csv(
        OUTPUT_DIR / "selected_building_metadata.csv",
        index=False
    )

    print("\n5. MATCHED BUILDING SAMPLE")
    print("------------------------------")

    sample_columns = [
        "building_id",
        "site_id",
        "primaryspaceusage",
        "sqm",
        "sqft",
        "yearbuilt",
        "numberoffloors",
        "timezone"
    ]

    print(
        matched_metadata[sample_columns]
        .head(10)
        .to_string(index=False)
    )

    print("\nMetadata inspection completed!")

    print("Reports saved in:", OUTPUT_DIR)


# --------------------------------------------------
# MAIN
# --------------------------------------------------

if __name__ == "__main__":
    inspect_metadata()
