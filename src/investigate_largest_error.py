
# Name: Mudassir Munir
# Roll No: PSEB-2026-010784
# Date: 2026-11-18

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parent.parent

ELECTRICITY_PATH = (
    ROOT / "data" / "cleaned" / "electricity_selected.csv"
)

PREDICTIONS_PATH = (
    ROOT / "outputs" / "reports" / "test_predictions.csv"
)

BUILDING_ID = "Hog_lodging_Shonda"

# This is the input timestamp associated with the large error.
ANOMALY_INPUT_TIME = pd.Timestamp("2017-11-05 01:00:00")


def main():
    predictions = pd.read_csv(
        PREDICTIONS_PATH,
        parse_dates=["timestamp"]
    )

    row = predictions.loc[
        predictions["timestamp"] == ANOMALY_INPUT_TIME
    ]

    if row.empty:
        raise ValueError("Anomaly timestamp not found in predictions.")

    prediction = row.iloc[0]

    print("\n--- Prediction Under Investigation ---")
    print(f"Input timestamp: {prediction['timestamp']}")
    print(f"Target timestamp: {prediction['timestamp'] + pd.Timedelta(hours=1)}")
    print(f"Actual target: {prediction['actual']}")
    print(
        "Predicted target: "
        f"{prediction['hist_gradient_boosting']:.4f}"
    )
    print(
        "Absolute error: "
        f"{abs(prediction['actual'] - prediction['hist_gradient_boosting']):.4f}"
    )

    print("\n--- Surrounding Electricity Readings ---")

    electricity = pd.read_csv(
        ELECTRICITY_PATH,
        usecols=["timestamp", BUILDING_ID],
        parse_dates=["timestamp"]
    )

    electricity = electricity.rename(
        columns={BUILDING_ID: "consumption"}
    )

    start = ANOMALY_INPUT_TIME - pd.Timedelta(hours=6)
    end = ANOMALY_INPUT_TIME + pd.Timedelta(hours=7)

    window = electricity.loc[
        electricity["timestamp"].between(start, end)
    ].copy()

    window["change_from_previous"] = (
        window["consumption"].diff()
    )

    print(
        window.to_string(
            index=False,
            formatters={
                "consumption": lambda value: f"{value:.2f}",
                "change_from_previous": (
                    lambda value: (
                        "" if pd.isna(value) else f"{value:.2f}"
                    )
                ),
            }
        )
    )

    print("\n--- Prediction Rows Around the Event ---")

    prediction_window = predictions.loc[
        predictions["timestamp"].between(start, end)
    ].copy()

    prediction_window["target_timestamp"] = (
        prediction_window["timestamp"]
        + pd.Timedelta(hours=1)
    )

    print(
        prediction_window[
            [
                "timestamp",
                "target_timestamp",
                "actual",
                "hist_gradient_boosting",
            ]
        ].to_string(index=False)
    )


if __name__ == "__main__":
    main()
