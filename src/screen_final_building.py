
# Name: Mudassir Munir
# Roll No: PSEB-2026-010784
# Date: 2026-11-18

"""
Screen complete electricity-meter columns to identify a
reliable candidate for next-hour electricity forecasting.

The screening considers:
- Missing readings
- Zero readings
- Monthly consumption stability
- Building metadata
"""

from pathlib import Path

import numpy as np
import pandas as pd


# --------------------------------------------------
# 1. Configuration
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

CHUNK_SIZE = 2000

REPORTS_DIR.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# 2. Read electricity data in chunks
# --------------------------------------------------

def screen_electricity_buildings():
    print("Screening electricity buildings...")

    header = pd.read_csv(ELECTRICITY_PATH, nrows=0)
    building_ids = [
        column for column in header.columns
        if column != "timestamp"
    ]

    missing_counts = pd.Series(0, index=building_ids, dtype="int64")
    zero_counts = pd.Series(0, index=building_ids, dtype="int64")

    monthly_sums = {}
    monthly_counts = {}

    total_rows = 0

    for chunk_number, chunk in enumerate(
        pd.read_csv(
            ELECTRICITY_PATH,
            chunksize=CHUNK_SIZE,
            parse_dates=["timestamp"]
        ),
        start=1
    ):
        total_rows += len(chunk)

        readings = chunk[building_ids]

        missing_counts += readings.isna().sum()
        zero_counts += readings.eq(0).sum()

        month_labels = chunk["timestamp"].dt.strftime("%Y-%m")

        for month, indexes in month_labels.groupby(month_labels).groups.items():
            month_readings = readings.loc[indexes]

            month_sum = month_readings.sum()
            month_count = month_readings.count()

            if month not in monthly_sums:
                monthly_sums[month] = month_sum
                monthly_counts[month] = month_count
            else:
                monthly_sums[month] += month_sum
                monthly_counts[month] += month_count

        print(
            f"Processed chunk {chunk_number} | "
            f"Rows processed: {total_rows:,}"
        )

    print(f"\nTotal rows processed: {total_rows:,}")

    return (
        building_ids,
        missing_counts,
        zero_counts,
        monthly_sums,
        monthly_counts,
        total_rows
    )


# --------------------------------------------------
# 3. Calculate monthly consumption stability
# --------------------------------------------------

def calculate_stability(
    building_ids,
    missing_counts,
    zero_counts,
    monthly_sums,
    monthly_counts,
    total_rows
):
    print("\nCalculating building stability...")

    monthly_means = {}

    for month in monthly_sums:
        monthly_means[month] = (
            monthly_sums[month]
            / monthly_counts[month].replace(0, np.nan)
        )

    monthly_df = pd.DataFrame(monthly_means).T
    monthly_df.index.name = "month"

    results = []

    for building_id in building_ids:
        missing = int(missing_counts[building_id])
        zeros = int(zero_counts[building_id])

        if missing != 0:
            continue

        month_changes = []

        for month_number in range(1, 13):
            month_2016 = f"2016-{month_number:02d}"
            month_2017 = f"2017-{month_number:02d}"

            if (
                month_2016 not in monthly_df.index
                or month_2017 not in monthly_df.index
            ):
                continue

            value_2016 = monthly_df.loc[month_2016, building_id]
            value_2017 = monthly_df.loc[month_2017, building_id]

            # Avoid misleading percentage changes when
            # the previous year's average is close to zero.
            if pd.isna(value_2016) or pd.isna(value_2017):
                continue

            if value_2016 <= 1:
                continue

            percentage_change = (
                (value_2017 - value_2016)
                / value_2016
            ) * 100

            month_changes.append(percentage_change)

        if not month_changes:
            continue

        results.append({
            "building_id": building_id,
            "missing_readings": missing,
            "zero_readings": zeros,
            "zero_percentage": zeros / total_rows * 100,
            "months_compared": len(month_changes),
            "median_absolute_monthly_change": np.median(
                np.abs(month_changes)
            ),
            "average_absolute_monthly_change": np.mean(
                np.abs(month_changes)
            )
        })

    result_df = pd.DataFrame(results)

    result_df = result_df.sort_values(
        by=[
            "median_absolute_monthly_change",
            "zero_percentage"
        ],
        ascending=True
    )

    return result_df


# --------------------------------------------------
# 4. Add building metadata
# --------------------------------------------------

def add_metadata(result_df):
    print("\nLoading building metadata...")

    metadata = pd.read_csv(METADATA_PATH)

    required_columns = [
        "building_id",
        "site_id",
        "primaryspaceusage",
        "sqm",
        "yearbuilt"
    ]

    available_columns = [
        column for column in required_columns
        if column in metadata.columns
    ]

    result_df = result_df.merge(
        metadata[available_columns],
        on="building_id",
        how="left"
    )

    return result_df


# --------------------------------------------------
# 5. Save and display results
# --------------------------------------------------

def save_results(result_df):
    output_path = (
        REPORTS_DIR / "final_building_screening_report.csv"
    )

    result_df.to_csv(output_path, index=False)

    print("\nTop 20 complete building candidates:")

    display_columns = [
        "building_id",
        "site_id",
        "primaryspaceusage",
        "missing_readings",
        "zero_percentage",
        "median_absolute_monthly_change",
        "average_absolute_monthly_change"
    ]

    display_columns = [
        column for column in display_columns
        if column in result_df.columns
    ]

    print(
        result_df[display_columns]
        .head(20)
        .round(2)
        .to_string(index=False)
    )

    print(f"\nTotal complete candidates: {len(result_df)}")
    print(f"Report saved: {output_path}")


# --------------------------------------------------
# 6. Main execution
# --------------------------------------------------

def main():
    (
        building_ids,
        missing_counts,
        zero_counts,
        monthly_sums,
        monthly_counts,
        total_rows
    ) = screen_electricity_buildings()

    result_df = calculate_stability(
        building_ids,
        missing_counts,
        zero_counts,
        monthly_sums,
        monthly_counts,
        total_rows
    )

    result_df = add_metadata(result_df)

    save_results(result_df)

    print("\n" + "=" * 55)
    print("FINAL BUILDING SCREENING COMPLETED")
    print("=" * 55)


if __name__ == "__main__":
    main()
