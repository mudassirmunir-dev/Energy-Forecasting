
# Name: Mudassir Munir
# Roll No: PSEB-2026-010784
# Date: 2026-11-18

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


ROOT = Path(__file__).resolve().parent.parent

PREDICTIONS_PATH = (
    ROOT / "outputs" / "reports" / "test_predictions.csv"
)

REPORT_DIR = ROOT / "outputs" / "reports"
FIGURE_DIR = ROOT / "outputs" / "figures"

BEST_MODEL = "hist_gradient_boosting"


def load_predictions():
    print("Loading model predictions...")

    df = pd.read_csv(
        PREDICTIONS_PATH,
        parse_dates=["timestamp"]
    )

    # The model predicts consumption for the following hour.
    df["target_timestamp"] = (
        df["timestamp"] + pd.Timedelta(hours=1)
    )

    df["error"] = (
        df["actual"] - df[BEST_MODEL]
    )

    df["absolute_error"] = df["error"].abs()

    df["target_month"] = (
        df["target_timestamp"].dt.to_period("M")
    )

    df["target_hour"] = (
        df["target_timestamp"].dt.hour
    )

    return df


def analyze_monthly_errors(df):
    monthly = (
        df.groupby("target_month")
        .agg(
            samples=("absolute_error", "count"),
            MAE=("absolute_error", "mean"),
            average_actual=("actual", "mean"),
            average_prediction=(BEST_MODEL, "mean"),
        )
        .round(4)
    )

    print("\n--- Monthly Error Analysis ---")
    print(monthly)

    monthly.to_csv(
        REPORT_DIR / "monthly_error_analysis.csv"
    )


def analyze_hourly_errors(df):
    hourly = (
        df.groupby("target_hour")
        .agg(
            samples=("absolute_error", "count"),
            MAE=("absolute_error", "mean"),
            average_actual=("actual", "mean"),
            average_prediction=(BEST_MODEL, "mean"),
        )
        .round(4)
    )

    print("\n--- Hourly Error Analysis ---")
    print(hourly)

    hourly.to_csv(
        REPORT_DIR / "hourly_error_analysis.csv"
    )


def analyze_largest_errors(df):
    largest = df.nlargest(
        20,
        "absolute_error"
    )[
        [
            "target_timestamp",
            "actual",
            BEST_MODEL,
            "error",
            "absolute_error",
        ]
    ].copy()

    numeric_columns = [
        "actual",
        BEST_MODEL,
        "error",
        "absolute_error",
    ]

    largest[numeric_columns] = (
        largest[numeric_columns].round(4)
    )

    print("\n--- 20 Largest Prediction Errors ---")
    print(largest.to_string(index=False))

    largest.to_csv(
        REPORT_DIR / "largest_prediction_errors.csv",
        index=False
    )


def create_visualizations(df):
    sns.set_theme(style="whitegrid")

    # Actual vs predicted
    plt.figure(figsize=(10, 6))

    sns.scatterplot(
        data=df,
        x="actual",
        y=BEST_MODEL,
        alpha=0.5
    )

    minimum = min(df["actual"].min(), df[BEST_MODEL].min())
    maximum = max(df["actual"].max(), df[BEST_MODEL].max())

    plt.plot(
        [minimum, maximum],
        [minimum, maximum],
        linestyle="--",
        label="Perfect prediction"
    )

    plt.xlabel("Actual Consumption")
    plt.ylabel("Predicted Consumption")
    plt.title("Actual vs Predicted Consumption")
    plt.legend()
    plt.tight_layout()

    plt.savefig(
        FIGURE_DIR / "actual_vs_predicted.png",
        dpi=300
    )
    plt.close()

    # Error distribution
    plt.figure(figsize=(10, 6))

    sns.histplot(
        data=df,
        x="error",
        bins=40,
        kde=True
    )

    plt.axvline(0, linestyle="--")

    plt.xlabel("Prediction Error (Actual - Predicted)")
    plt.title("Prediction Error Distribution")
    plt.tight_layout()

    plt.savefig(
        FIGURE_DIR / "prediction_error_distribution.png",
        dpi=300
    )
    plt.close()

    # Monthly MAE
    monthly = (
        df.groupby("target_month")["absolute_error"]
        .mean()
        .reset_index()
    )

    monthly["target_month"] = (
        monthly["target_month"].astype(str)
    )

    plt.figure(figsize=(10, 6))

    sns.barplot(
        data=monthly,
        x="target_month",
        y="absolute_error"
    )

    plt.xticks(rotation=45)
    plt.xlabel("Target Month")
    plt.ylabel("MAE")
    plt.title("Monthly Prediction Error")
    plt.tight_layout()

    plt.savefig(
        FIGURE_DIR / "monthly_prediction_error.png",
        dpi=300
    )
    plt.close()

    print("\nUpdated plots saved.")


def save_summary(df):
    mae = df["absolute_error"].mean()
    rmse = (df["error"].pow(2).mean()) ** 0.5
    bias = df["error"].mean()

    summary = f"""
MODEL ERROR ANALYSIS SUMMARY
============================

Model: {BEST_MODEL}

Total test predictions: {len(df)}

MAE: {mae:.4f}
RMSE: {rmse:.4f}
Mean Error (Actual - Predicted): {bias:.4f}

Positive error means underprediction.
Negative error means overprediction.

IMPORTANT:
Errors are grouped using target_timestamp,
not the input timestamp.

Forecasting setup:
One-step-ahead predictions using actual
recent consumption readings as historical inputs.
"""

    output_path = (
        REPORT_DIR / "error_analysis_summary.txt"
    )

    output_path.write_text(
        summary,
        encoding="utf-8"
    )

    print("\n" + summary)
    print(f"Summary saved: {output_path}")


def main():
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)

    df = load_predictions()

    analyze_monthly_errors(df)
    analyze_hourly_errors(df)
    analyze_largest_errors(df)

    create_visualizations(df)
    save_summary(df)

    print("\nERROR ANALYSIS COMPLETED")


if __name__ == "__main__":
    main()
