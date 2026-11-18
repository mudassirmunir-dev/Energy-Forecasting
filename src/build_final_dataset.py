
# Name: Mudassir Munir
# Roll No: PSEB-2026-010784
# Date: 2026-11-18

"""
Build a supervised next-hour electricity forecasting dataset.

Prediction:
Use information available at hour t to predict electricity
consumption at hour t+1.

The script does not impute missing weather values.
Imputation will be performed inside the sklearn pipeline
after the chronological train/test split.
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

WEATHER_PATH = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "bdg2"
    / "weather.csv"
)

OUTPUT_DIR = PROJECT_ROOT / "data" / "cleaned"
REPORTS_DIR = PROJECT_ROOT / "outputs" / "reports"

OUTPUT_PATH = OUTPUT_DIR / "final_forecasting_dataset.csv"
REPORT_PATH = REPORTS_DIR / "final_dataset_report.txt"

BUILDING_ID = "Hog_lodging_Shonda"
SITE_ID = "Hog"

WEATHER_FEATURES = [
    "airTemperature",
    "dewTemperature",
    "windSpeed",
    "windDirection",
    "seaLvlPressure",
]


# --------------------------------------------------
# 2. Load electricity readings
# --------------------------------------------------

def load_electricity():
    print("Loading selected building electricity data...")

    data = pd.read_csv(
        ELECTRICITY_PATH,
        usecols=["timestamp", BUILDING_ID],
        parse_dates=["timestamp"]
    )

    data = data.rename(
        columns={BUILDING_ID: "consumption"}
    )

    data = data.sort_values("timestamp").reset_index(drop=True)

    if data["timestamp"].duplicated().any():
        raise ValueError("Duplicate electricity timestamps found.")

    if data["consumption"].isna().any():
        raise ValueError("Missing electricity readings found.")

    if (data["consumption"] < 0).any():
        raise ValueError("Negative electricity readings found.")

    print(f"Electricity rows: {len(data):,}")

    return data


# --------------------------------------------------
# 3. Load site weather data
# --------------------------------------------------

def load_weather():
    print("\nLoading site weather data...")

    weather = pd.read_csv(
        WEATHER_PATH,
        parse_dates=["timestamp"]
    )

    weather = weather.loc[
        weather["site_id"] == SITE_ID
    ].copy()

    available_features = [
        column for column in WEATHER_FEATURES
        if column in weather.columns
    ]

    if not available_features:
        raise ValueError("No expected weather features were found.")

    weather = weather[
        ["timestamp"] + available_features
    ]

    weather = weather.sort_values("timestamp").reset_index(drop=True)

    if weather["timestamp"].duplicated().any():
        raise ValueError(
            "Duplicate weather timestamps found for site "
            f"{SITE_ID}. Investigate before merging."
        )

    print(f"Weather rows for site {SITE_ID}: {len(weather):,}")
    print(f"Weather features: {available_features}")

    return weather, available_features


# --------------------------------------------------
# 4. Create forecasting features
# --------------------------------------------------

def create_features(data):
    print("\nCreating time-series features...")

    data = data.sort_values("timestamp").copy()

    # The target is electricity consumption one hour ahead.
    data["target_timestamp"] = (
        data["timestamp"] + pd.Timedelta(hours=1)
    )

    data["target"] = data["consumption"].shift(-1)

    # Consumption history available at the current timestamp.
    data["consumption_lag_1"] = data["consumption"]
    data["consumption_lag_24"] = data["consumption"].shift(23)
    data["consumption_lag_168"] = data["consumption"].shift(167)

    # Rolling windows include the current reading,
    # which is available when predicting the next hour.
    data["rolling_mean_24"] = (
        data["consumption"]
        .rolling(window=24, min_periods=24)
        .mean()
    )

    data["rolling_mean_168"] = (
        data["consumption"]
        .rolling(window=168, min_periods=168)
        .mean()
    )

    # Calendar features describe the hour being predicted.
    target_time = data["target_timestamp"]

    data["hour"] = target_time.dt.hour
    data["day_of_week"] = target_time.dt.dayofweek
    data["month"] = target_time.dt.month
    data["day_of_month"] = target_time.dt.day
    data["is_weekend"] = (
        target_time.dt.dayofweek >= 5
    ).astype(int)

    # Remove rows without enough historical information
    # or without a next-hour target.
    data = data.dropna(
        subset=[
            "target",
            "consumption_lag_24",
            "consumption_lag_168",
            "rolling_mean_24",
            "rolling_mean_168",
        ]
    ).copy()

    return data


# --------------------------------------------------
# 5. Merge weather with electricity features
# --------------------------------------------------

def merge_weather(data, weather, weather_features):
    print("\nMerging electricity and weather data...")

    merged = data.merge(
        weather,
        on="timestamp",
        how="left",
        validate="one_to_one",
        indicator=True
    )

    merged["weather_matched"] = (
        merged["_merge"] == "both"
    ).astype(int)

    unmatched_count = int(
        (merged["_merge"] == "left_only").sum()
    )

    merged = merged.drop(columns=["_merge"])

    print(f"Rows without matching weather: {unmatched_count:,}")

    for column in weather_features:
        missing = int(merged[column].isna().sum())

        print(
            f"{column}: {missing:,} missing "
            f"({missing / len(merged) * 100:.2f}%)"
        )

    return merged


# --------------------------------------------------
# 6. Select final columns
# --------------------------------------------------

def select_final_columns(data, weather_features):
    feature_columns = [
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
    ] + weather_features

    final_columns = [
        "timestamp",
        "target_timestamp",
    ] + feature_columns + ["target"]

    return data[final_columns].copy()


# --------------------------------------------------
# 7. Generate report
# --------------------------------------------------

def generate_report(data, weather_features):
    feature_columns = [
        column for column in data.columns
        if column not in [
            "timestamp",
            "target_timestamp",
            "target"
        ]
    ]

    lines = [
        "FINAL FORECASTING DATASET REPORT",
        "=" * 45,
        f"Building: {BUILDING_ID}",
        f"Site: {SITE_ID}",
        "Prediction task: Next-hour electricity consumption",
        "",
        f"Rows: {len(data):,}",
        f"Columns: {len(data.columns):,}",
        f"Features: {len(feature_columns):,}",
        f"Target: target",
        "",
        f"First input timestamp: {data['timestamp'].min()}",
        f"Last input timestamp: {data['timestamp'].max()}",
        f"First target timestamp: {data['target_timestamp'].min()}",
        f"Last target timestamp: {data['target_timestamp'].max()}",
        "",
        "Missing values by column:",
        data.isna().sum().to_string(),
        "",
        "Feature columns:",
        "\n".join(feature_columns),
        "",
        "Weather features:",
        "\n".join(weather_features),
        "",
        "Target statistics:",
        data["target"].describe().to_string(),
        "",
        "Important:",
        "- Weather missing values have not been imputed.",
        "- Imputation must be fitted on training data only.",
        "- Use chronological splitting, not random splitting.",
        "- Do not use timestamp columns as model features.",
    ]

    REPORT_PATH.write_text(
        "\n".join(lines),
        encoding="utf-8"
    )


# --------------------------------------------------
# 8. Main
# --------------------------------------------------

def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    electricity = load_electricity()

    weather, weather_features = load_weather()

    featured = create_features(electricity)

    final_data = merge_weather(
        featured,
        weather,
        weather_features
    )

    final_data = select_final_columns(
        final_data,
        weather_features
    )

    final_data.to_csv(OUTPUT_PATH, index=False)

    generate_report(
        final_data,
        weather_features
    )

    print("\n" + "=" * 55)
    print("FINAL FORECASTING DATASET CREATED")
    print("=" * 55)

    print(f"Rows: {len(final_data):,}")
    print(f"Columns: {len(final_data.columns):,}")
    print(f"Saved: {OUTPUT_PATH}")
    print(f"Report: {REPORT_PATH}")

    print("\nDataset preview:")
    print(final_data.head().to_string(index=False))

    print("\nMissing values:")
    print(final_data.isna().sum().to_string())


if __name__ == "__main__":
    main()
