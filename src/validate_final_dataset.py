
# Name: Mudassir Munir
# Roll No: PSEB-2026-010784
# Date: 2026-11-18

from pathlib import Path

import pandas as pd
import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATASET_PATH = (
    PROJECT_ROOT
    / "data"
    / "cleaned"
    / "final_forecasting_dataset.csv"
)

REPORT_PATH = (
    PROJECT_ROOT
    / "outputs"
    / "reports"
    / "final_dataset_validation.txt"
)


def main():
    print("Loading final forecasting dataset...")

    data = pd.read_csv(
        DATASET_PATH,
        parse_dates=["timestamp", "target_timestamp"]
    )

    print("\n1. Dataset shape")
    print(f"Rows: {data.shape[0]:,}")
    print(f"Columns: {data.shape[1]}")

    print("\n2. Column data types")
    print(data.dtypes.to_string())

    print("\n3. First five rows")
    print(data.head().to_string(index=False))

    print("\n4. Numeric column validation")

    numeric_columns = [
        "consumption_lag_1",
        "consumption_lag_24",
        "consumption_lag_168",
        "rolling_mean_24",
        "rolling_mean_168",
        "hour",
        "day_of_week",
        "month",
        "day_of_month",
        "is_weekend",
        "weather_matched",
        "airTemperature",
        "dewTemperature",
        "windSpeed",
        "windDirection",
        "seaLvlPressure",
        "target",
    ]

    conversion_errors = {}

    for column in numeric_columns:
        converted = pd.to_numeric(
            data[column],
            errors="coerce"
        )

        errors = int(
            (converted.isna() & data[column].notna()).sum()
        )

        conversion_errors[column] = errors

        print(
            f"{column}: "
            f"dtype={data[column].dtype}, "
            f"conversion errors={errors}"
        )

    print("\n5. Timestamp validation")

    chronological = data["timestamp"].is_monotonic_increasing
    unique_timestamps = data["timestamp"].is_unique

    expected_target = (
        data["timestamp"] + pd.Timedelta(hours=1)
    )

    target_alignment = (
        data["target_timestamp"] == expected_target
    ).all()

    print(f"Chronological order: {chronological}")
    print(f"Unique input timestamps: {unique_timestamps}")
    print(f"Target timestamps correctly aligned: {target_alignment}")

    print("\n6. Target validation")

    print(data["target"].describe().round(3).to_string())

    print(f"Missing target values: {data['target'].isna().sum()}")
    print(f"Negative target values: {(data['target'] < 0).sum()}")

    print("\n7. Missing values")

    missing = data.isna().sum()
    print(missing[missing > 0].to_string() or "No missing values")

    print("\n8. Duplicate rows")

    duplicate_rows = int(data.duplicated().sum())
    print(f"Duplicate rows: {duplicate_rows}")

    print("\n9. Validation summary")

    checks = {
        "Expected row count": len(data) > 0,
        "Chronological order": chronological,
        "Unique timestamps": unique_timestamps,
        "Target timestamp alignment": target_alignment,
        "No missing target": data["target"].notna().all(),
        "No negative target": (data["target"] >= 0).all(),
        "No duplicate rows": duplicate_rows == 0,
        "No numeric conversion errors": all(
            errors == 0 for errors in conversion_errors.values()
        ),
    }

    for name, passed in checks.items():
        print(f"{'PASS' if passed else 'FAIL'}: {name}")

    report_lines = [
        "FINAL DATASET VALIDATION REPORT",
        "=" * 45,
        f"Rows: {len(data)}",
        f"Columns: {len(data.columns)}",
        "",
        "Data types:",
        data.dtypes.to_string(),
        "",
        "Missing values:",
        data.isna().sum().to_string(),
        "",
        "Validation checks:",
    ]

    report_lines.extend(
        f"{'PASS' if passed else 'FAIL'}: {name}"
        for name, passed in checks.items()
    )

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

    REPORT_PATH.write_text(
        "\n".join(report_lines),
        encoding="utf-8"
    )

    print(f"\nReport saved: {REPORT_PATH}")


if __name__ == "__main__":
    main()
