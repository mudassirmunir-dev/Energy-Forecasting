
# Name: Mudassir Munir
# Roll No: PSEB-2026-010784
# Date: 2026-11-18

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# --------------------------------------------------
# PROJECT PATHS
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

ELECTRICITY_FILE = (
    BASE_DIR / "data" / "cleaned"
    / "electricity_selected.csv"
)

FIGURES_DIR = BASE_DIR / "outputs" / "figures"
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

BUILDING_ID = "Robin_office_Wai"


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

def load_data():

    df = pd.read_csv(
        ELECTRICITY_FILE,
        usecols=["timestamp", BUILDING_ID],
        parse_dates=["timestamp"]
    )

    df = df.sort_values("timestamp")

    return df


# --------------------------------------------------
# PLOT FULL ELECTRICITY TIME SERIES
# --------------------------------------------------

def plot_full_timeseries(df):

    plt.figure(figsize=(15, 6))

    plt.plot(
        df["timestamp"],
        df[BUILDING_ID],
        linewidth=0.5
    )

    plt.title(
        f"Hourly Electricity Consumption - {BUILDING_ID}"
    )

    plt.xlabel("Timestamp")
    plt.ylabel("Electricity Reading")

    plt.grid(alpha=0.3)
    plt.tight_layout()

    output_file = (
        FIGURES_DIR / "robin_office_electricity_timeseries.png"
    )

    plt.savefig(output_file, dpi=150)
    plt.close()

    print(f"Saved: {output_file}")


# --------------------------------------------------
# PLOT ZERO READING PERIODS
# --------------------------------------------------

def plot_zero_periods(df):

    zero_rows = df[df[BUILDING_ID] == 0]

    plt.figure(figsize=(15, 5))

    plt.plot(
        df["timestamp"],
        df[BUILDING_ID],
        linewidth=0.5,
        label="Electricity readings"
    )

    plt.scatter(
        zero_rows["timestamp"],
        zero_rows[BUILDING_ID],
        color="red",
        s=18,
        label="Zero readings"
    )

    plt.title("Zero Electricity Reading Periods")
    plt.xlabel("Timestamp")
    plt.ylabel("Electricity Reading")

    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()

    output_file = (
        FIGURES_DIR / "robin_office_zero_readings.png"
    )

    plt.savefig(output_file, dpi=150)
    plt.close()

    print(f"Saved: {output_file}")


# --------------------------------------------------
# MAIN
# --------------------------------------------------

if __name__ == "__main__":

    print("Loading building electricity data...")

    electricity = load_data()

    plot_full_timeseries(electricity)

    plot_zero_periods(electricity)

    print("\nVisualization completed!")
