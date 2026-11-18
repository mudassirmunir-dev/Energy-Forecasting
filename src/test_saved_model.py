
# Name: Mudassir Munir
# Roll No: PSEB-2026-010784
# Date: 2026-11-18

from pathlib import Path

import joblib
import pandas as pd
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)


ROOT = Path(__file__).resolve().parent.parent

MODEL_PATH = ROOT / "models" / "hist_gradient_boosting.joblib"

DATA_PATH = (
    ROOT / "data" / "cleaned" / "final_forecasting_dataset.csv"
)

OUTPUT_PATH = (
    ROOT / "outputs" / "reports" / "saved_model_predictions.csv"
)

FEATURE_COLUMNS = [
    "consumption_lag_1",
    "consumption_lag_24",
    "consumption_lag_168",
    "rolling_mean_24",
    "rolling_mean_168",
    "day_of_month",
    "airTemperature",
    "dewTemperature",
    "windSpeed",
    "windDirection",
    "seaLvlPressure",
    "hour",
    "day_of_week",
    "month",
    "is_weekend",
    "weather_matched",
]


def main():
    print("Loading saved model...")

    model = joblib.load(MODEL_PATH)

    print("Model loaded successfully.")

    print("\nLoading original forecasting dataset...")

    df = pd.read_csv(
        DATA_PATH,
        parse_dates=["timestamp", "target_timestamp"]
    )

    print(f"Dataset rows: {len(df)}")

    # Validate that all expected features exist.
    missing_features = [
        col for col in FEATURE_COLUMNS
        if col not in df.columns
    ]

    if missing_features:
        raise ValueError(
            f"Missing model features: {missing_features}"
        )

    # Separate input features and target.
    X = df[FEATURE_COLUMNS]
    y = df["target"]

    # Recreate the same chronological 80/20 split.
    split_index = int(len(df) * 0.80)

    X_test = X.iloc[split_index:]
    y_test = y.iloc[split_index:]

    test_timestamps = df["target_timestamp"].iloc[
        split_index:
    ]

    print(f"\nTraining rows: {split_index}")
    print(f"Testing rows: {len(X_test)}")

    print("\nGenerating predictions using saved model...")

    predictions = model.predict(X_test)

    results = pd.DataFrame({
        "target_timestamp": test_timestamps.to_numpy(),
        "actual": y_test.to_numpy(),
        "predicted": predictions,
    })

    results["error"] = (
        results["actual"] - results["predicted"]
    )

    results["absolute_error"] = results["error"].abs()

    # Calculate evaluation metrics.
    mae = mean_absolute_error(y_test, predictions)

    rmse = mean_squared_error(
        y_test,
        predictions
    ) ** 0.5

    r2 = r2_score(y_test, predictions)

    print("\n--- Sample Predictions ---")

    print(
        results.head(10).round(4).to_string(index=False)
    )

    print("\n--- Saved Model Evaluation ---")

    print(f"MAE:  {mae:.4f}")
    print(f"RMSE: {rmse:.4f}")
    print(f"R2:   {r2:.4f}")

    # Save predictions.
    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    results.to_csv(
        OUTPUT_PATH,
        index=False
    )

    print(f"\nPredictions saved to: {OUTPUT_PATH}")

    print("\nSAVED MODEL TEST COMPLETED")


if __name__ == "__main__":
    main()
