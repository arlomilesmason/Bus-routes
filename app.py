import streamlit as st
import pandas as pd
import os

st.set_page_config(layout="wide")
st.title("Bus Transport Analysis Dashboard")

# ========================
# LOAD DATA
# ========================

freq_path = "outputs/data/frequency.csv"
route_path = "outputs/data/routes.csv"
journeys_path = "outputs/data/journeys.csv"  # ✅ needed for optimisation

if not os.path.exists(freq_path) or not os.path.exists(route_path):
    st.warning("Run main.py first")
    st.stop()

freq_df = pd.read_csv(freq_path)
route_df = pd.read_csv(route_path)

# Optional journeys data (for optimisation)
if os.path.exists(journeys_path):
    journeys_df = pd.read_csv(journeys_path)
else:
    journeys_df = None


# ========================
# SIDEBAR
# ========================

st.sidebar.header("Controls")

routes = sorted(route_df["route"].unique())
selected_route = st.sidebar.selectbox("Select Route", ["ALL"] + routes)

# ========================
# FILTER DATA
# ========================

if selected_route == "ALL":
    filtered_routes = route_df.copy()
    filtered_journeys = journeys_df.copy() if journeys_df is not None else None
else:
    filtered_routes = route_df[route_df["route"] == selected_route]

    if journeys_df is not None:
        filtered_journeys = journeys_df[journeys_df["route"] == selected_route]
    else:
        filtered_journeys = None


# ========================
# SUMMARY
# ========================

st.header("Summary")

col1, col2, col3 = st.columns(3)

col1.metric("Total Journeys", len(route_df))
col2.metric("Routes", len(routes))

peak_hour = freq_df.loc[freq_df["journeys"].idxmax(), "hour"]
col3.metric("Peak Hour", f"{peak_hour}:00")


# ========================
# FREQUENCY
# ========================

st.header("Service Frequency")
st.line_chart(freq_df.set_index("hour")["journeys"])


# ========================
# ROUTE ANALYSIS
# ========================

st.header("Route Analysis")

if selected_route == "ALL":
    st.info("Select a route")
else:
    route_hourly = filtered_routes.groupby("hour")["journeys"].sum().reset_index()
    st.line_chart(route_hourly.set_index("hour")["journeys"])

    st.write("Peak hours:")
    st.write(route_hourly.sort_values("journeys", ascending=False).head())


# ========================
# HEATMAPS
# ========================

st.header("Service Heatmap")

if os.path.exists("outputs/maps/heatmap.html"):
    st.components.v1.html(open("outputs/maps/heatmap.html", encoding="utf-8").read(), height=600)

st.header("Passenger Demand Heatmap")

if os.path.exists("outputs/maps/demand_heatmap.html"):
    st.components.v1.html(open("outputs/maps/demand_heatmap.html", encoding="utf-8").read(), height=600)


# ========================
# ROUTE MAP
# ========================

st.header("Route Map")

map_file = "outputs/maps/routes_map.html"

if selected_route != "ALL":
    specific = f"outputs/maps/route_{selected_route}.html"
    if os.path.exists(specific):
        map_file = specific

if os.path.exists(map_file):
    with open(map_file, encoding="utf-8") as f:
        st.components.v1.html(f.read(), height=600)
else:
    st.warning("Run main.py to generate map")


# ========================
# OPTIMISATION (FIXED ✅)
# ========================

st.header("Optimisation Insights")

if filtered_journeys is not None and "passengers" in filtered_journeys.columns:

    # Compute stats LIVE (correct approach)
    stats = filtered_journeys.groupby("route").agg(
        avg_passengers=("passengers", "mean"),
        total_passengers=("passengers", "sum"),
        journeys=("route", "count")
    ).reset_index()

    # Fix operators ✅
    overused = stats[stats["avg_passengers"] > 50]
    underused = stats[stats["avg_passengers"] < 15]

    col1, col2 = st.columns(2)

    col1.subheader("Overcrowded Routes")
    col1.write(overused)

    col2.subheader("Underused Routes")
    col2.write(underused)

else:
    st.info("Run simulation in main.py to enable optimisation")


# ========================
# STATISTICS
# ========================

st.header("Statistical Insights")

mean = freq_df["journeys"].mean()
std = freq_df["journeys"].std()

st.write(f"Mean demand: {mean:.2f}")
st.write(f"Std deviation: {std:.2f}")

peak = freq_df.loc[freq_df["journeys"].idxmax()]

st.write(
    f"Peak hour: {int(peak['hour'])}:00 ({int(peak['journeys'])} journeys)"
)

# Correct operators ✅
within = freq_df[
    (freq_df["journeys"] >= mean - std) &
    (freq_df["journeys"] <= mean + std)
]

st.write(
    f"{len(within)}/24 hours fall within 1 std dev (normal distribution behaviour)"
)

# ========================
# FOOTER
# ========================

st.markdown("---")
st.write("Transport Analytics & Optimisation Project")
