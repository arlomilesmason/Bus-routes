import numpy as np


def simulate_passenger_demand(journeys_df, capacity=60):
    """
    Simulate passengers using normal distribution + peak weighting
    """

    peak_hour = 13  # midday peak

    passengers = []

    for _, row in journeys_df.iterrows():
        hour = row["hour"]

        # Peak weighting
        weight = np.exp(-((hour - peak_hour) ** 2) / 10)

        value = np.random.normal(
            loc=capacity * 0.5 * (1 + weight),
            scale=10
        )

        value = max(0, min(capacity * 1.5, value))  # bounds

        passengers.append(value)

    journeys_df["passengers"] = passengers

    return journeys_df
