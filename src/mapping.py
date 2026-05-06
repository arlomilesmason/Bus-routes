import folium
from folium.plugins import HeatMap
import random

# ✅ Warwickshire bounds
WARKS_BOUNDS = {
    "min_lat": 52.1,
    "max_lat": 52.6,
    "min_lon": -1.9,
    "max_lon": -1.2
}


def in_warwickshire(lat, lon):
    return (
        WARKS_BOUNDS["min_lat"] <= lat <= WARKS_BOUNDS["max_lat"] and
        WARKS_BOUNDS["min_lon"] <= lon <= WARKS_BOUNDS["max_lon"]
    )


def route_in_warwickshire(coords):
    return any(in_warwickshire(lat, lon) for lat, lon in coords)


def generate_color():
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))


# =====================================
# ✅ ROUTE MAP (LINES + COLOURS)
# =====================================
def create_route_map(routes, selected_route=None,
                     output_file="outputs/maps/routes_map.html"):

    if not routes:
        print("No route data")
        return

    # ✅ Filter by geography
    routes = [r for r in routes if route_in_warwickshire(r["coords"])]

    if selected_route:
        routes = [r for r in routes if r["route"] == selected_route]

    if not routes:
        print("No valid Warwickshire routes")
        return

    all_coords = [c for r in routes for c in r["coords"]]

    center_lat = sum(lat for lat, _ in all_coords) / len(all_coords)
    center_lon = sum(lon for _, lon in all_coords) / len(all_coords)

    m = folium.Map(location=[center_lat, center_lon], zoom_start=11)

    route_colors = {}
    legend_html = "<b>Route Legend</b><br>"

    for route in routes:
        name = route["route"]

        if name not in route_colors:
            route_colors[name] = generate_color()

        folium.PolyLine(
            route["coords"],
            color=route_colors[name],
            weight=4,
            opacity=0.8,
            tooltip=f"Route {name}"   # ✅ hover
        ).add_to(m)

    # ✅ Legend
    for name, color in route_colors.items():
        legend_html += f'<div><span style="color:{color};">■</span> {name}</div>'

    legend = folium.Element(f"""
    <div style="
        position: fixed;
        bottom: 50px;
        left: 50px;
        background: white;
        padding: 10px;
        border: 2px solid grey;
        z-index: 9999;
    ">
        {legend_html}
    </div>
    """)

    m.get_root().html.add_child(legend)

    m.save(output_file)
    print(f"✅ Route map saved → {output_file}")


# =====================================
# 🔥 FREQUENCY HEATMAP
# =====================================
def create_frequency_heatmap(routes, journeys_df,
                             output_file="outputs/maps/heatmap.html"):

    if not routes or journeys_df.empty:
        print("No data for heatmap")
        return

    route_counts = journeys_df.groupby("route").size().to_dict()

    heat_data = []

    for route in routes:
        name = route["route"]

        if name not in route_counts:
            continue

        weight = route_counts[name]

        for lat, lon in route["coords"]:
            if in_warwickshire(lat, lon):
                heat_data.append([lat, lon, weight])

    if not heat_data:
        print("No Warwickshire data for heatmap")
        return

    avg_lat = sum(p[0] for p in heat_data) / len(heat_data)
    avg_lon = sum(p[1] for p in heat_data) / len(heat_data)

    m = folium.Map(location=[avg_lat, avg_lon], zoom_start=11)

    HeatMap(heat_data, radius=8, blur=15).add_to(m)

    m.save(output_file)
    print(f"✅ Frequency heatmap saved → {output_file}")


# =====================================
# 🧍 DEMAND HEATMAP
# =====================================
def create_demand_heatmap(routes, journeys_df,
                          output_file="outputs/maps/demand_heatmap.html"):

    if "passengers" not in journeys_df.columns:
        print("No passenger data")
        return

    route_passengers = journeys_df.groupby("route")["passengers"].sum().to_dict()

    heat_data = []

    for route in routes:
        name = route["route"]

        if name not in route_passengers:
            continue

        weight = route_passengers[name]

        for lat, lon in route["coords"]:
            if in_warwickshire(lat, lon):
                heat_data.append([lat, lon, weight])

    if not heat_data:
        print("No demand data for Warwickshire")
        return

    avg_lat = sum(p[0] for p in heat_data) / len(heat_data)
    avg_lon = sum(p[1] for p in heat_data) / len(heat_data)

    m = folium.Map(location=[avg_lat, avg_lon], zoom_start=11)

    HeatMap(heat_data, radius=10, blur=20).add_to(m)

    m.save(output_file)
    print(f"✅ Demand heatmap saved → {output_file}")