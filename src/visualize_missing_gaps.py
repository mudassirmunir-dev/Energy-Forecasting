
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

DATA_FILE = (
    BASE_DIR
    / "data"
    / "cleaned"
    / "electricity_selected.csv"
)

GAP_REPORT = (
    BASE_DIR
    / "outputs"
    / "reports"
    / "missing_gap_analysis.csv"
)

OUTPUT_DIR = BASE_DIR / "outputs" / "figures"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

TOP_N = 5


# --------------------------------------------------
# VISUALIZE MISSING GAPS
# --------------------------------------------------

def visualize_missing_gaps():

    print("Loading missing-gap report...")

    report = pd.read_csv(GAP_REPORT)

    # Select buildings with the longest continuous gaps
    top_buildings = (
        report.sort_values(
            by="Longest Gap (Hours)",
            ascending=False
        )
        .head(TOP_N)["Building ID"]
        .tolist()
    )

    print("\nSelected buildings:")

    for building in top_buildings:
        print(building)

    # Load timestamps and selected building columns
    columns = ["timestamp"] + top_buildings

    print("\nLoading electricity readings...")

    df = pd.read_csv(
        DATA_FILE,
        usecols=columns,
        parse_dates=["timestamp"]
    )

    df = df.sort_values("timestamp")

    # Create one subplot per building
    fig, axes = plt.subplots(
        TOP_N,
        1,
        figsize=(15, 12),
        sharex=True
    )

    for ax, building in zip(axes, top_buildings):

        missing_mask = df[building].isna()

        # Plot available readings
        ax.plot(
            df["timestamp"],
            df[building],
            linewidth=0.7
        )

        # Mark missing timestamps
        ax.scatter(
            df.loc[missing_mask, "timestamp"],
            [0] * missing_mask.sum(),
            marker="x",
            s=8,
            label="Missing readings"
        )

        ax.set_title(building)
        ax.set_ylabel("Reading")
        ax.grid(True, alpha=0.3)

    axes[-1].set_xlabel("Timestamp")

    fig.suptitle(
        "Electricity Missing-Data Patterns - Top 5 Buildings",
        fontsize=15
    )

    plt.tight_layout()

    output_file = (
        OUTPUT_DIR / "missing_gaps_top_5_buildings.png"
    )

    plt.savefig(
        output_file,
        dpi=300,
        bbox_inches="tight"
    )

    plt.show()

    print("\nVisualization completed!")
    print(f"Chart saved to: {output_file}")


# --------------------------------------------------
# MAIN EXECUTION
# --------------------------------------------------

if __name__ == "__main__":
    visualize_missing_gaps()
