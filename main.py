import os

from src.parser import parse_folder
from src.transform import clean_data
from src.analysis import (
    service_frequency,
    route_frequency,
    frequency_distribution
)
from src.visualisation import (
    plot_frequency,
    plot_normal_distribution,
    plot_clusters
)
from src.clustering import cluster_time_of_day
from src.mapping import (
    create_route_map,
    create_frequency_heatmap,
    create_demand_heatmap
)
from src.simulation import simulate_passenger_demand
from src.optimisation import (
    calculate_route_stats,
    identify_issues,
    identify_peak_pressure,
    network_summary
)


def main():
    print(" Starting pipeline...")

    # ========================
    # ✅ SETUP OUTPUT FOLDERS
    # ========================
    os.makedirs("outputs/data", exist_ok=True)
    os.makedirs("outputs/plots", exist_ok=True)
    os.makedirs("outputs/maps", exist_ok=True)

    # ========================
    # ✅ LOAD DATA
    # ========================
    journeys, routes = parse_folder("Timetabledata")

    print(f"\nLoaded journeys: {len(journeys)}")
    print(f"Loaded route segments: {len(routes)}")

    # ========================
    # ✅ CLEAN DATA
    # ========================
    journeys = clean_data(journeys)

    # ========================
    # ✅ ANALYSIS
    # ========================
    freq_df = service_frequency(journeys)
    route_df = route_frequency(journeys)

    mean, std = frequency_distribution(freq_df)

    print("\n Frequency Stats")
    print(f"Mean journeys/hour: {mean:.2f}")
    print(f"Std deviation: {std:.2f}")

    # ========================
    # ✅ CLUSTERING
    # ========================
    freq_df, centers = cluster_time_of_day(freq_df)

    print("\n Cluster centers:")
    print(centers)

    # ========================
    # ✅ SIMULATE PASSENGERS (CRITICAL!)
    # ========================
    journeys = simulate_passenger_demand(journeys)

    print("\n✅ Passenger simulation complete")

    # ========================
    # ✅ OPTIMISATION
    # ========================
    route_stats = calculate_route_stats(journeys)
    issues = identify_issues(route_stats)
    peaks = identify_peak_pressure(journeys)
    summary = network_summary(route_stats)

    print("\n Optimisation Summary:")
    print(summary)

    print("\n Route Issues:")
    print(issues)

    print("\nPeak Demand Hours:")
    print(peaks)

    # ========================
    # ✅ SAVE DATA (IMPORTANT FOR DASHBOARD)
    # ========================
    journeys.to_csv("outputs/data/journeys.csv", index=False)  # ✅ REQUIRED FIX
    freq_df.to_csv("outputs/data/frequency.csv", index=False)
    route_df.to_csv("outputs/data/routes.csv", index=False)

    print("✅ Data saved")

    # ========================
    # ✅ VISUALISATIONS
    # ========================
    plot_frequency(freq_df, "outputs/plots/frequency.png")
    plot_normal_distribution(freq_df, "outputs/plots/normal.png")
    plot_clusters(freq_df, "outputs/plots/clusters.png")

    print("✅ Plots generated")

    # ========================
    # ✅ MAPS
    # ========================
    create_route_map(routes)
    create_frequency_heatmap(routes, journeys)
    create_demand_heatmap(routes, journeys)

    print("✅ Maps generated")

    print("\n Pipeline complete!")


if __name__ == "__main__":
    main()
