import pandas as pd


def calculate_route_stats(journeys_df):
    """
    Aggregate journeys and passengers per route
    """
    stats = journeys_df.groupby("route").agg(
        journeys=("route", "count"),
        total_passengers=("passengers", "sum"),
        avg_passengers=("passengers", "mean")
    ).reset_index()

    return stats


def identify_issues(route_stats):
    """
    Identify overloaded and underused routes
    """
    issues = []

    for _, row in route_stats.iterrows():
        if row["avg_passengers"] > 50:
            issues.append({
                "route": row["route"],
                "issue": "Overcrowded",
                "recommendation": "Increase service frequency"
            })

        elif row["avg_passengers"] < 15:
            issues.append({
                "route": row["route"],
                "issue": "Underused",
                "recommendation": "Reduce frequency or review route"
            })

    return pd.DataFrame(issues)


def identify_peak_pressure(journeys_df):
    """
    Identify busiest hours with high passenger demand
    """
    hourly = journeys_df.groupby("hour")["passengers"].sum().reset_index()

    peak_hours = hourly.sort_values("passengers", ascending=False).head(5)

    return peak_hours


def network_summary(route_stats):
    return {
        "total_routes": len(route_stats),
        "total_passengers": int(route_stats["total_passengers"].sum()),
        "avg_passengers_per_route": round(route_stats["avg_passengers"].mean(), 2)
    }
