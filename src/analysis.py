import scipy.stats as stats


def service_frequency(journeys_df):
    return journeys_df.groupby("hour").size().reset_index(name="journeys")


def route_frequency(journeys_df):
    return journeys_df.groupby(["route", "hour"]).size().reset_index(name="journeys")


def service_summary(journeys_df):
    return {
        "total_journeys": len(journeys_df),
        "first_bus": journeys_df["departure_time"].min().strftime("%H:%M"),
        "last_bus": journeys_df["departure_time"].max().strftime("%H:%M")
    }


def frequency_distribution(freq_df):
    mean = freq_df["journeys"].mean()
    std = freq_df["journeys"].std()
    return mean, std


def probability_range(freq_df):
    mean = freq_df["journeys"].mean()
    std = freq_df["journeys"].std()

    return stats.norm.cdf(mean + std, mean, std) - stats.norm.cdf(mean - std, mean, std)