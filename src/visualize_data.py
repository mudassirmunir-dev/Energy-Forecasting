
# Name: Mudassir Munir
# Roll No: PSEB-2026-010784
# Date: 2026-11-18

from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "raw" / "bdg2"
FIGURES_DIR = BASE_DIR / "outputs" / "figures"

FIGURES_DIR.mkdir(parents=True, exist_ok=True)


def plot_electricity_consumption():
    """Plot average electricity readings over time."""

    file_path = DATA_DIR / "electricity.csv"

    timestamps = []
    average_readings = []

    # Read electricity data in smaller chunks
    for chunk in pd.read_csv(file_path, chunksize=2000):

        chunk["timestamp"] = pd.to_datetime(chunk["timestamp"])

        building_data = chunk.iloc[:, 1:]

        # Calculate average across buildings for each timestamp
        row_average = building_data.mean(axis=1)

        timestamps.extend(chunk["timestamp"])
        average_readings.extend(row_average)

    plt.figure(figsize=(14, 5))
    plt.plot(timestamps, average_readings)

    plt.title("Average Electricity Readings Over Time")
    plt.xlabel("Timestamp")
    plt.ylabel("Average Meter Reading")
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.savefig(FIGURES_DIR / "electricity_over_time.png")
    plt.close()

    print("Saved electricity_over_time.png")


def plot_weather_missing_values():
    """Visualize missing values in weather columns."""

    file_path = DATA_DIR / "weather.csv"

    weather = pd.read_csv(file_path)

    missing_percentage = (
        weather.isnull().mean() * 100
    ).sort_values(ascending=False)

    plt.figure(figsize=(12, 6))
    missing_percentage.plot(kind="bar")

    plt.title("Missing Values in Weather Dataset")
    plt.xlabel("Weather Columns")
    plt.ylabel("Missing Values (%)")
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.savefig(FIGURES_DIR / "weather_missing_values.png")
    plt.close()

    print("Saved weather_missing_values.png")


def plot_building_usage():
    """Visualize the distribution of building types."""

    file_path = DATA_DIR / "metadata" / "metadata.csv"

    metadata = pd.read_csv(file_path)

    usage_counts = (
        metadata["primaryspaceusage"]
        .fillna("Unknown")
        .value_counts()
        .head(10)
    )

    plt.figure(figsize=(12, 6))
    usage_counts.plot(kind="bar")

    plt.title("Building Distribution by Primary Usage")
    plt.xlabel("Building Usage")
    plt.ylabel("Number of Buildings")
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.savefig(FIGURES_DIR / "building_usage_distribution.png")
    plt.close()

    print("Saved building_usage_distribution.png")


def main():
    plot_electricity_consumption()
    plot_weather_missing_values()
    plot_building_usage()

    print("\nAll visualizations generated successfully!")


if __name__ == "__main__":
    main()
