
# Name: Mudassir Munir
# Roll No: PSEB-2026-010784
# Date: 2026-11-18

"""
Analyze test-set prediction errors for the trained models.
"""

from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


PROJECT_ROOT = Path(__file__).resolve().parent.parent

PREDICTIONS_PATH = (
    PROJECT_ROOT
    / "outputs"
    / "reports"
    / "test_predictions.csv"
)

FIGURES_DIR = PROJECT_ROOT / "outputs" / "figures"
REPORTS_DIR = PROJECT_ROOT / "outputs" / "reports"

BEST_MODEL = "hist_gradient_boosting"

FIGURES_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)


def load_predictions():
    data = pd.read_csv(
        PREDICTIONS_PATH,
        parse_dates=["timestamp"]
    )

    data = data.sort_values("timestamp").reset_index(drop=True)

    required = [
        "timestamp",
        "actual",
        "persistence_baseline",
        "random_forest",
        "hist_gradient_boosting",
    ]

    missing = [column for column in required if column not in data.columns]

    if missing:
        raise ValueError(f"Missing prediction columns: {missing}")

    return data


def calculate_errors(data):
    data = data.copy()

    data["error"] = data["actual"] - data[BEST_MODEL]
    data["absolute_error"] = data["error"].abs()

    data["month"] = data["timestamp"].dt.strftime("%Y-%m")
    data["hour"] = data["timestamp"].dt.hour

    return data


def analyze_by_month(data):
    monthly = data.groupby("month").agg(
        samples=("actual", "size"),
        MAE=("absolute_error", "mean"),
        average_actual=("actual", "mean"),
        average_prediction=(BEST_MODEL, "mean"),
    )

    monthly["MAE"] = monthly["MAE"].round(4)
    monthly["average_actual"] = monthly["average_actual"].round(4)
    monthly["average_prediction"] = monthly["average_prediction"].round(4)

    output = REPORTS_DIR / "monthly_error_analysis.csv"
    monthly.to_csv(output)

    print("\n--- Monthly Error Analysis ---")
    print(monthly.to_string())
    print(f"Saved: {output}")

    return monthly


def analyze_by_hour(data):
    hourly = data.groupby("hour").agg(
        samples=("actual", "size"),
        MAE=("absolute_error", "mean"),
        average_actual=("actual", "mean"),
        average_prediction=(BEST_MODEL, "mean"),
    )

    hourly["MAE"] = hourly["MAE"].round(4)
    hourly["average_actual"] = hourly["average_actual"].round(4)
    hourly["average_prediction"] = hourly["average_prediction"].round(4)

    output = REPORTS_DIR / "hourly_error_analysis.csv"
    hourly.to_csv(output)

    print("\n--- Hourly Error Analysis ---")
    print(hourly.to_string())
    print(f"Saved: {output}")

    return hourly


def save_largest_errors(data):
    largest = data.nlargest(20, "absolute_error")[
        [
            "timestamp",
            "actual",
            BEST_MODEL,
            "error",
            "absolute_error",
        ]
    ].copy()

    largest = largest.round(4)

    output = REPORTS_DIR / "largest_prediction_errors.csv"
    largest.to_csv(output, index=False)

    print("\n--- 20 Largest Prediction Errors ---")
    print(largest.to_string(index=False))
    print(f"Saved: {output}")


def create_plots(data, monthly):
    # Actual vs predicted over the test period.
    plt.figure(figsize=(14, 5))
    plt.plot(
        data["timestamp"],
        data["actual"],
        label="Actual",
        linewidth=1
    )
    plt.plot(
        data["timestamp"],
        data[BEST_MODEL],
        label="Predicted",
        linewidth=1
    )
    plt.title("Actual vs Predicted Electricity Consumption")
    plt.xlabel("Timestamp")
    plt.ylabel("Electricity Consumption")
    plt.legend()
    plt.tight_layout()

    plt.savefig(
        FIGURES_DIR / "actual_vs_predicted.png",
        dpi=150
    )
    plt.close()

    # Residual distribution.
    plt.figure(figsize=(9, 5))
    plt.hist(data["error"], bins=40, edgecolor="black")
    plt.axvline(0, linestyle="--", linewidth=1)
    plt.title("Prediction Error Distribution")
    plt.xlabel("Error (Actual - Predicted)")
    plt.ylabel("Frequency")
    plt.tight_layout()

    plt.savefig(
        FIGURES_DIR / "prediction_error_distribution.png",
        dpi=150
    )
    plt.close()

    # Monthly MAE.
    plt.figure(figsize=(11, 5))
    plt.bar(monthly.index.astype(str), monthly["MAE"])
    plt.title("Monthly Prediction Error (MAE)")
    plt.xlabel("Month")
    plt.ylabel("Mean Absolute Error")
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.savefig(
        FIGURES_DIR / "monthly_prediction_error.png",
        dpi=150
    )
    plt.close()

    print("\nPlots saved:")
    print("outputs/figures/actual_vs_predicted.png")
    print("outputs/figures/prediction_error_distribution.png")
    print("outputs/figures/monthly_prediction_error.png")


def save_summary(data, monthly, hourly):
    summary = [
        "MODEL ERROR ANALYSIS",
        "=" * 45,
        f"Model: {BEST_MODEL}",
        f"Test samples: {len(data):,}",
        f"Overall MAE: {data['absolute_error'].mean():.4f}",
        f"Mean error (bias): {data['error'].mean():.4f}",
        f"Maximum absolute error: {data['absolute_error'].max():.4f}",
        "",
        "Worst month by MAE:",
        monthly["MAE"].idxmax(),
        f"MAE: {monthly['MAE'].max():.4f}",
        "",
        "Worst hour by MAE:",
        str(hourly["MAE"].idxmax()),
        f"MAE: {hourly['MAE'].max():.4f}",
        "",
        "Interpretation:",
        "Positive error means the model underpredicted.",
        "Negative error means the model overpredicted.",
    ]

    output = REPORTS_DIR / "error_analysis_summary.txt"
    output.write_text("\n".join(summary), encoding="utf-8")

    print(f"\nSummary saved: {output}")


def main():
    print("Loading model predictions...")

    data = load_predictions()
    data = calculate_errors(data)

    monthly = analyze_by_month(data)
    hourly = analyze_by_hour(data)

    save_largest_errors(data)
    create_plots(data, monthly)
    save_summary(data, monthly, hourly)

    print("\nERROR ANALYSIS COMPLETED")


if __name__ == "__main__":
    main()
