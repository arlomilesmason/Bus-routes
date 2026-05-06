import pandas as pd


def clean_data(journeys_df):
    journeys_df["departure_time"] = pd.to_datetime(
        journeys_df["departure_time"],
        format="%H:%M:%S",
        errors="coerce"
    )

    journeys_df = journeys_df.dropna(subset=["departure_time"])
    journeys_df["hour"] = journeys_df["departure_time"].dt.hour

    return journeys_df