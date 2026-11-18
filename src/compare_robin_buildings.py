
# Name: Mudassir Munir
# Roll No: PSEB-2026-010784
# Date: 2026-11-18

"""
Compare electricity consumption at Robin site buildings
to investigate whether the 2017 drop was building-specific
or shared across the site.
"""

from pathlib import Path

import pandas as pd


# --------------------------------------------------
# 1. Paths and configuration
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

ELECTRICITY_PATH = (
    PROJECT_ROOT
    / "data"
    / "cleaned"
    / "electricity_selected.csv"
)

METADATA_PATH = (
    PROJECT_ROOT
    / "outputs"
    / "reports"
    / "selected_building_metadata.csv"
)

REPORTS_DIR = PROJECT_ROOT / "outputs" / "reports"

TARGET_BUILDING = "Robin_office_Wai"
TARGET_SITE = "Robin"

REPORTS_DIR.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# 2. Load metadata and find Robin buildings
# --------------------------------------------------

def load_robin_buildings():
    print("Loading selected building metadata...")

    metadata = pd.read_csv(METADATA_PATH)

    robin_metadata = metadata[
        metadata["site_id"].astype(str) == TARGET_SITE
    ].copy()

    building_ids = robin_metadata["building_id"].dropna().tolist()

    print(f"Buildings listed at Robin site: {len(building_ids)}")

    return robin_metadata, building_ids


# --------------------------------------------------
# 3. Load electricity readings
# --------------------------------------------------

def load_electricity(building_ids):
    print("\nLoading electricity readings...")

    available_columns = pd.read_csv(
        ELECTRICITY_PATH,
        nrows=0
    ).columns.tolist()

    selected_buildings = [
        building_id
        for building_id in building_ids
        if building_id in available_columns
    ]

    if TARGET_BUILDING not in selected_buildings:
        raise ValueError(
            f"{TARGET_BUILDING} was not found in the selected dataset."
        )

    print(
        f"Robin buildings available in electricity data: "
        f"{len(selected_buildings)}"
    )

    df = pd.read_csv(
        ELECTRICITY_PATH,
        usecols=["timestamp"] + selected_buildings,
        parse_dates=["timestamp"]
    )

    print(f"Total hourly records: {len(df):,}")

    return df, selected_buildings


# --------------------------------------------------
# 4. Convert readings into long format
# --------------------------------------------------

def convert_to_long_format(df, building_ids):
    print("\nConverting selected buildings to long format...")

    long_df = df.melt(
        id_vars=["timestamp"],
        value_vars=building_ids,
        var_name="building_id",
        value_name="electricity"
    )

    long_df["year"] = long_df["timestamp"].dt.year
    long_df["month"] = long_df["timestamp"].dt.month

    print(f"Long-format records: {len(long_df):,}")

    return long_df


# --------------------------------------------------
# 5. Compare May-July across years
# --------------------------------------------------

def compare_periods(long_df, metadata):
    print("\nComparing May-July 2016 against May-July 2017...")

    period_df = long_df[
        long_df["month"].isin([5, 6, 7])
        & long_df["year"].isin([2016, 2017])
    ].copy()

    summary = (
        period_df.groupby(["building_id", "year"])
        .agg(
            average_reading=("electricity", "mean"),
            median_reading=("electricity", "median"),
            missing_readings=("electricity", lambda x: x.isna().sum()),
            zero_readings=("electricity", lambda x: (x == 0).sum()),
            valid_readings=("electricity", "count")
        )
        .reset_index()
    )

    average_comparison = summary.pivot(
        index="building_id",
        columns="year",
        values="average_reading"
    )

    median_comparison = summary.pivot(
        index="building_id",
        columns="year",
        values="median_reading"
    )

    average_comparison = average_comparison.rename(
        columns={
            2016: "average_2016",
            2017: "average_2017"
        }
    )

    median_comparison = median_comparison.rename(
        columns={
            2016: "median_2016",
            2017: "median_2017"
        }
    )

    comparison = average_comparison.join(median_comparison)

    comparison["percentage_change"] = (
        (
            comparison["average_2017"]
            - comparison["average_2016"]
        )
        / comparison["average_2016"]
    ) * 100

    comparison = comparison.reset_index()

    comparison = comparison.merge(
        metadata[["building_id", "primaryspaceusage", "sqm"]],
        on="building_id",
        how="left"
    )

    comparison = comparison.sort_values(
        "percentage_change"
    )

    output_path = (
        REPORTS_DIR / "robin_site_building_comparison.csv"
    )

    comparison.to_csv(output_path, index=False)

    print("\nBuilding comparison results:")
    print(
        comparison[
            [
                "building_id",
                "average_2016",
                "average_2017",
                "percentage_change"
            ]
        ].round(2).to_string(index=False)
    )

    print(f"\nReport saved: {output_path}")

    return comparison


# --------------------------------------------------
# 6. Compare target building with site-wide behaviour
# --------------------------------------------------

def print_site_summary(comparison):
    print("\nSite-wide comparison summary:")

    valid = comparison.dropna(
        subset=["percentage_change"]
    )

    print(f"Buildings compared: {len(valid)}")

    if valid.empty:
        print("No valid building comparisons available.")
        return

    print(
        "Buildings with decreased average readings: "
        f"{(valid['percentage_change'] < 0).sum()}"
    )

    print(
        "Buildings with increased average readings: "
        f"{(valid['percentage_change'] > 0).sum()}"
    )

    print(
        "Median percentage change across buildings: "
        f"{valid['percentage_change'].median():.2f}%"
    )

    target = valid[
        valid["building_id"] == TARGET_BUILDING
    ]

    if not target.empty:
        print(
            f"{TARGET_BUILDING} percentage change: "
            f"{target.iloc[0]['percentage_change']:.2f}%"
        )


# --------------------------------------------------
# 7. Main execution
# --------------------------------------------------

def main():
    metadata, building_ids = load_robin_buildings()

    electricity, available_buildings = load_electricity(
        building_ids
    )

    long_df = convert_to_long_format(
        electricity,
        available_buildings
    )

    comparison = compare_periods(
        long_df,
        metadata
    )

    print_site_summary(comparison)

    print("\n" + "=" * 55)
    print("ROBIN SITE COMPARISON COMPLETED")
    print("=" * 55)


if __name__ == "__main__":
    main()
