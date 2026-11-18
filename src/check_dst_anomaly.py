
# Name: Mudassir Munir
# Roll No: PSEB-2026-010784
# Date: 2026-11-18

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parent.parent

ELECTRICITY_PATH = (
    ROOT / "data" / "cleaned" / "electricity_selected.csv"
)

BUILDING_ID = "Hog_lodging_Shonda"


def main():
    df = pd.read_csv(
        ELECTRICITY_PATH,
        usecols=["timestamp", BUILDING_ID],
        parse_dates=["timestamp"]
    )

    df = df.rename(columns={BUILDING_ID: "consumption"})

    dates_to_check = [
        "2017-11-04",
        "2017-11-05",
        "2017-11-06",
        "2016-11-06",
    ]

    for date in dates_to_check:
        day = pd.Timestamp(date)

        result = df.loc[
            df["timestamp"].dt.date == day.date()
        ].copy()

        print(f"\n--- {date} ---")
        print(f"Number of readings: {len(result)}")

        print(
            result[
                ["timestamp", "consumption"]
            ].to_string(index=False)
        )

    print("\n--- Same Hour Comparison ---")

    selected = df.loc[
        (df["timestamp"].dt.month == 11)
        & (df["timestamp"].dt.day == 5)
        & (df["timestamp"].dt.hour == 2)
    ]

    print(selected.to_string(index=False))


if __name__ == "__main__":
    main()
