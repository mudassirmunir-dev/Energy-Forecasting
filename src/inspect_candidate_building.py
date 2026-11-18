
# Name: Mudassir Munir
# Roll No: PSEB-2026-010784
# Date: 2026-11-18

import pandas as pd
from pathlib import Path

# --------------------------------------------------
# PROJECT CONFIGURATION
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

ELECTRICITY_FILE = (
    BASE_DIR / "data" / "cleaned"
    / "electricity_selected.csv"
)

WEATHER_FILE = (
    BASE_DIR / "data" / "raw" / "bdg2"
    / "weather.csv"
)

OUTPUT_DIR = BASE_DIR / "outputs" / "reports"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

BUILDING_ID = "Robin_office_Wai"
SITE_ID = "Robin"


# --------------------------------------------------
# INSPECT ELECTRICITY READINGS
# --------------------------------------------------

def inspect_electricity():

    print("\n1. ELECTRICITY DATA")
    print("=" * 50)

    electricity = pd.read_csv(
        ELECTRICITY_FILE,
        usecols=["timestamp", BUILDING_ID],
        parse_dates=["timestamp"]
    )

    electricity = electricity.sort_values("timestamp")

    readings = electricity[BUILDING_ID]

    print(f"Building: {BUILDING_ID}")
    print(f"Total records: {len(electricity)}")
    print(f"Missing readings: {readings.isna().sum()}")
    print(f"Unique readings: {readings.nunique()}")
    print(f"Zero readings: {(readings == 0).sum()}")
    print(f"Negative readings: {(readings < 0).sum()}")

    print(f"\nFirst timestamp: {electricity['timestamp'].min()}")
    print(f"Last timestamp: {electricity['timestamp'].max()}")

    print("\nElectricity statistics:")
    print(readings.describe().to_string())

    return electricity


# --------------------------------------------------
# INSPECT WEATHER DATA
# --------------------------------------------------

def inspect_weather():

    print("\n2. WEATHER DATA")
    print("=" * 50)

    weather = pd.read_csv(WEATHER_FILE)

    weather["timestamp"] = pd.to_datetime(
        weather["timestamp"],
        errors="coerce"
    )

    site_weather = weather[
        weather["site_id"].astype(str) == SITE_ID
    ].copy()

    site_weather = site_weather.sort_values("timestamp")

    print(f"Site: {SITE_ID}")
    print(f"Total weather records for site: {len(site_weather)}")

    print(
        f"First weather timestamp: "
        f"{site_weather['timestamp'].min()}"
    )

    print(
        f"Last weather timestamp: "
        f"{site_weather['timestamp'].max()}"
    )

    print("\nMissing weather values:")
    print(site_weather.isna().sum().to_string())

    print(
        "\nDuplicate weather timestamps:",
        site_weather["timestamp"].duplicated().sum()
    )

    return site_weather


# --------------------------------------------------
# CHECK TIMESTAMP MATCHING
# --------------------------------------------------

def check_timestamp_matching(electricity, weather):

    print("\n3. ELECTRICITY AND WEATHER ALIGNMENT")
    print("=" * 50)

    electricity_timestamps = set(
        electricity["timestamp"].dropna()
    )

    weather_timestamps = set(
        weather["timestamp"].dropna()
    )

    matched = electricity_timestamps & weather_timestamps

    electricity_only = (
        electricity_timestamps - weather_timestamps
    )

    weather_only = (
        weather_timestamps - electricity_timestamps
    )

    print(
        f"Electricity timestamps: "
        f"{len(electricity_timestamps)}"
    )

    print(
        f"Weather timestamps: "
        f"{len(weather_timestamps)}"
    )

    print(f"Matching timestamps: {len(matched)}")
    print(f"Electricity-only timestamps: {len(electricity_only)}")
    print(f"Weather-only timestamps: {len(weather_only)}")

    # --------------------------------------------------
    # SAVE ALIGNMENT REPORT
    # --------------------------------------------------

    report = pd.DataFrame({
        "Metric": [
            "Building ID",
            "Site ID",
            "Electricity timestamps",
            "Weather timestamps",
            "Matching timestamps",
            "Electricity-only timestamps",
            "Weather-only timestamps"
        ],
        "Value": [
            BUILDING_ID,
            SITE_ID,
            len(electricity_timestamps),
            len(weather_timestamps),
            len(matched),
            len(electricity_only),
            len(weather_only)
        ]
    })

    report.to_csv(
        OUTPUT_DIR / "candidate_alignment_report.csv",
        index=False
    )

    print("\nAlignment report saved.")


# --------------------------------------------------
# MAIN
# --------------------------------------------------

if __name__ == "__main__":

    electricity = inspect_electricity()

    weather = inspect_weather()

    check_timestamp_matching(
        electricity,
        weather
    )

    print("\nCandidate inspection completed!")
