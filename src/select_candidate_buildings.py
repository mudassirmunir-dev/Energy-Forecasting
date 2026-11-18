
# Name: Mudassir Munir
# Roll No: PSEB-2026-010784
# Date: 2026-11-18

import pandas as pd
from pathlib import Path

# --------------------------------------------------
# PROJECT PATHS
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

ELECTRICITY_REPORT = (
    BASE_DIR / "outputs" / "reports"
    / "selected_missing_report.csv"
)

METADATA_FILE = (
    BASE_DIR / "outputs" / "reports"
    / "selected_building_metadata.csv"
)

OUTPUT_DIR = BASE_DIR / "outputs" / "reports"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# SELECT CANDIDATE BUILDINGS
# --------------------------------------------------

def select_candidate_buildings():

    print("Loading building reports...")

    electricity = pd.read_csv(
        ELECTRICITY_REPORT,
        index_col=0
    )

    metadata = pd.read_csv(METADATA_FILE)

    # --------------------------------------------------
    # PREPARE ELECTRICITY MISSING-VALUE REPORT
    # --------------------------------------------------

    electricity.index = electricity.index.astype(str)

    electricity.index.name = "building_id"

    electricity = electricity.reset_index()

    electricity = electricity.rename(columns={
        "Missing Values": "missing_count",
        "Missing Percentage": "missing_percentage"
    })

    electricity = electricity[
        electricity["building_id"] != "timestamp"
    ]

    # --------------------------------------------------
    # MERGE ELECTRICITY AND METADATA
    # --------------------------------------------------

    metadata["building_id"] = (
        metadata["building_id"].astype(str)
    )

    candidates = electricity.merge(
        metadata,
        on="building_id",
        how="inner",
        validate="one_to_one"
    )

    # --------------------------------------------------
    # CHECK BUILDING ELIGIBILITY
    # --------------------------------------------------

    candidates["has_valid_usage"] = (
        candidates["primaryspaceusage"].notna()
    )

    candidates["has_valid_site"] = (
        candidates["site_id"].notna()
    )

    candidates["has_valid_area"] = (
        candidates["sqm"].notna()
        & (candidates["sqm"] > 0)
    )

    candidates["has_complete_electricity"] = (
        candidates["missing_percentage"] == 0
    )

    # --------------------------------------------------
    # CREATE A SIMPLE SELECTION SCORE
    # --------------------------------------------------

    candidates["selection_score"] = (
        candidates["has_complete_electricity"].astype(int)
        + candidates["has_valid_usage"].astype(int)
        + candidates["has_valid_site"].astype(int)
        + candidates["has_valid_area"].astype(int)
    )

    # Rank complete electricity readings first,
    # then use metadata completeness as a tie-breaker.
    candidates = candidates.sort_values(
        by=[
            "has_complete_electricity",
            "selection_score",
            "missing_percentage"
        ],
        ascending=[False, False, True]
    )

    # --------------------------------------------------
    # DISPLAY RESULTS
    # --------------------------------------------------

    print("\n1. CANDIDATE SUMMARY")
    print("------------------------------")

    print(
        f"Total matched buildings: {len(candidates)}"
    )

    print(
        "Buildings with complete electricity readings:",
        int(candidates["has_complete_electricity"].sum())
    )

    print(
        "Buildings with valid area:",
        int(candidates["has_valid_area"].sum())
    )

    print(
        "Buildings with valid usage:",
        int(candidates["has_valid_usage"].sum())
    )

    print("\n2. TOP 20 CANDIDATE BUILDINGS")
    print("------------------------------")

    display_columns = [
        "building_id",
        "site_id",
        "primaryspaceusage",
        "sqm",
        "missing_count",
        "missing_percentage",
        "selection_score"
    ]

    print(
        candidates[display_columns]
        .head(20)
        .to_string(index=False)
    )

    # --------------------------------------------------
    # SAVE REPORT
    # --------------------------------------------------

    output_file = (
        OUTPUT_DIR / "candidate_buildings_report.csv"
    )

    candidates[display_columns].to_csv(
        output_file,
        index=False
    )

    print("\nCandidate report saved:")
    print(output_file)


# --------------------------------------------------
# MAIN
# --------------------------------------------------

if __name__ == "__main__":
    select_candidate_buildings()
