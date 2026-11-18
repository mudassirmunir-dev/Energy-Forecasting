
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

INPUT_FILE = BASE_DIR / "outputs" / "reports" / "selected_missing_report.csv"
OUTPUT_DIR = BASE_DIR / "outputs" / "figures"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# VISUALIZE MISSING VALUES
# --------------------------------------------------

def visualize_missing_values():

    print("Loading missing-value report...")

    report = pd.read_csv(INPUT_FILE, index_col=0)

    # Keep only columns that have missing values
    missing_data = report[
        report["Missing Percentage"] > 0
    ].sort_values(
        by="Missing Percentage",
        ascending=False
    )

    # Top 20 buildings
    top_20 = missing_data.head(20)

    plt.figure(figsize=(12, 7))

    plt.barh(
        top_20.index[::-1],
        top_20["Missing Percentage"][::-1]
    )

    plt.title("Top 20 Buildings by Missing Data")
    plt.xlabel("Missing Values (%)")
    plt.ylabel("Building ID")

    plt.tight_layout()

    output_file = OUTPUT_DIR / "top_20_missing_buildings.png"

    plt.savefig(output_file, dpi=300)
    plt.show()

    print(f"\nChart saved to: {output_file}")


# --------------------------------------------------
# MAIN EXECUTION
# --------------------------------------------------

if __name__ == "__main__":
    visualize_missing_values()
