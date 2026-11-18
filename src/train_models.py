
# Name: Mudassir Munir
# Roll No: PSEB-2026-010784
# Date: 2026-11-18

"""
Train and evaluate next-hour electricity forecasting models.

Models:
1. Persistence baseline
2. Random Forest Regressor
3. HistGradientBoosting Regressor

Uses a chronological 80/20 train-test split.
All preprocessing is fitted only on training data.
"""

from pathlib import Path

import joblib
import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import (
    RandomForestRegressor,
    HistGradientBoostingRegressor,
)
from sklearn.impute import SimpleImputer
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


# --------------------------------------------------
# 1. Paths and configuration
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATASET_PATH = (
    PROJECT_ROOT
    / "data"
    / "cleaned"
    / "final_forecasting_dataset.csv"
)

MODEL_DIR = PROJECT_ROOT / "models"
REPORT_DIR = PROJECT_ROOT / "outputs" / "reports"

MODEL_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)

TEST_SIZE = 0.20
RANDOM_STATE = 42


# --------------------------------------------------
# 2. Define features
# --------------------------------------------------

NUMERIC_FEATURES = [
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
]

CATEGORICAL_FEATURES = [
    "hour",
    "day_of_week",
    "month",
    "is_weekend",
    "weather_matched",
]

FEATURE_COLUMNS = NUMERIC_FEATURES + CATEGORICAL_FEATURES
TARGET_COLUMN = "target"


# --------------------------------------------------
# 3. Load dataset and split chronologically
# --------------------------------------------------

def load_and_split_data():
    print("Loading final forecasting dataset...")

    data = pd.read_csv(
        DATASET_PATH,
        parse_dates=["timestamp", "target_timestamp"]
    )

    data = data.sort_values("timestamp").reset_index(drop=True)

    X = data[FEATURE_COLUMNS]
    y = data[TARGET_COLUMN]

    split_index = int(len(data) * (1 - TEST_SIZE))

    X_train = X.iloc[:split_index].copy()
    X_test = X.iloc[split_index:].copy()

    y_train = y.iloc[:split_index].copy()
    y_test = y.iloc[split_index:].copy()

    train_timestamps = data["timestamp"].iloc[:split_index]
    test_timestamps = data["timestamp"].iloc[split_index:]

    print(f"\nTotal samples: {len(data):,}")
    print(f"Training samples: {len(X_train):,}")
    print(f"Testing samples: {len(X_test):,}")

    print(
        f"\nTraining period: "
        f"{train_timestamps.min()} to {train_timestamps.max()}"
    )

    print(
        f"Testing period: "
        f"{test_timestamps.min()} to {test_timestamps.max()}"
    )

    return X_train, X_test, y_train, y_test, test_timestamps


# --------------------------------------------------
# 4. Create preprocessing pipeline
# --------------------------------------------------

def create_preprocessor():
    numeric_pipeline = Pipeline([
        (
            "imputer",
            SimpleImputer(strategy="median")
        )
    ])

    categorical_pipeline = Pipeline([
        (
            "imputer",
            SimpleImputer(strategy="most_frequent")
        ),
        (
            "encoder",
            OneHotEncoder(
                handle_unknown="ignore",
                sparse_output=False
            )
        )
    ])

    preprocessor = ColumnTransformer([
        (
            "numeric",
            numeric_pipeline,
            NUMERIC_FEATURES
        ),
        (
            "categorical",
            categorical_pipeline,
            CATEGORICAL_FEATURES
        ),
    ])

    return preprocessor


# --------------------------------------------------
# 5. Define ML models
# --------------------------------------------------

def create_models():
    models = {
        "random_forest": RandomForestRegressor(
            n_estimators=200,
            max_depth=15,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=RANDOM_STATE,
            n_jobs=-1,
        ),

        "hist_gradient_boosting": HistGradientBoostingRegressor(
            max_iter=200,
            learning_rate=0.08,
            max_leaf_nodes=20,
            l2_regularization=1.0,
            random_state=RANDOM_STATE,
        ),
    }

    return models


# --------------------------------------------------
# 6. Evaluation metrics
# --------------------------------------------------

def evaluate_predictions(y_true, predictions):
    mae = mean_absolute_error(y_true, predictions)

    rmse = np.sqrt(
        mean_squared_error(y_true, predictions)
    )

    r2 = r2_score(y_true, predictions)

    return {
        "MAE": mae,
        "RMSE": rmse,
        "R2": r2,
    }


# --------------------------------------------------
# 7. Train and evaluate models
# --------------------------------------------------

def train_and_evaluate(
    X_train,
    X_test,
    y_train,
    y_test,
    test_timestamps,
):
    results = []
    prediction_data = pd.DataFrame({
        "timestamp": test_timestamps.reset_index(drop=True),
        "actual": y_test.reset_index(drop=True),
    })

    # Persistence baseline:
    # Predict the next hour using the latest known reading.
    baseline_predictions = X_test[
        "consumption_lag_1"
    ].to_numpy()

    baseline_metrics = evaluate_predictions(
        y_test,
        baseline_predictions
    )

    results.append({
        "model": "persistence_baseline",
        **baseline_metrics,
    })

    prediction_data["persistence_baseline"] = (
        baseline_predictions
    )

    print("\nPersistence baseline:")
    print(pd.Series(baseline_metrics).round(4).to_string())

    models = create_models()

    for model_name, model in models.items():
        print(f"\nTraining {model_name}...")

        pipeline = Pipeline([
            ("preprocessor", create_preprocessor()),
            ("model", model),
        ])

        pipeline.fit(X_train, y_train)

        predictions = pipeline.predict(X_test)

        metrics = evaluate_predictions(
            y_test,
            predictions
        )

        results.append({
            "model": model_name,
            **metrics,
        })

        prediction_data[model_name] = predictions

        model_path = MODEL_DIR / f"{model_name}.joblib"

        joblib.dump(pipeline, model_path)

        print(f"{model_name} results:")
        print(pd.Series(metrics).round(4).to_string())
        print(f"Saved model: {model_path}")

    return pd.DataFrame(results), prediction_data


# --------------------------------------------------
# 8. Save reports and predictions
# --------------------------------------------------

def save_results(results, prediction_data):
    results = results.sort_values(
        by="MAE",
        ascending=True
    )

    results_path = REPORT_DIR / "model_comparison.csv"
    predictions_path = REPORT_DIR / "test_predictions.csv"

    results.to_csv(results_path, index=False)
    prediction_data.to_csv(predictions_path, index=False)

    print("\n" + "=" * 60)
    print("MODEL COMPARISON")
    print("=" * 60)

    print(results.round(4).to_string(index=False))

    print(f"\nMetrics saved: {results_path}")
    print(f"Predictions saved: {predictions_path}")


# --------------------------------------------------
# 9. Main
# --------------------------------------------------

def main():
    (
        X_train,
        X_test,
        y_train,
        y_test,
        test_timestamps,
    ) = load_and_split_data()

    results, predictions = train_and_evaluate(
        X_train,
        X_test,
        y_train,
        y_test,
        test_timestamps,
    )

    save_results(results, predictions)

    print("\nMODEL TRAINING COMPLETED")


if __name__ == "__main__":
    main()
