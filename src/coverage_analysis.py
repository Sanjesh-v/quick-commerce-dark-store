import pandas as pd
from geopy.distance import geodesic
import folium
from pathlib import Path

# ----------------------------------
# Parameters
# ----------------------------------

SERVICE_RADIUS = 3  # km

# ----------------------------------
# Load Data
# ----------------------------------

demand = pd.read_csv(
    "data/processed/clustered_demand.csv"
)

stores = pd.read_csv(
    "data/raw/existing_dark_stores.csv"
)

# ----------------------------------
# Nearest Store Function
# ----------------------------------

def nearest_store_distance(lat, lon):

    point = (lat, lon)

    distances = []

    for _, store in stores.iterrows():

        store_point = (
            store["Latitude"],
            store["Longitude"]
        )

        dist = geodesic(
            point,
            store_point
        ).km

        distances.append(dist)

    return min(distances)

# ----------------------------------
# Calculate Distances
# ----------------------------------

demand["Nearest_Store_Distance"] = demand.apply(
    lambda row:
    nearest_store_distance(
        row["Latitude"],
        row["Longitude"]
    ),
    axis=1
)

# ----------------------------------
# Coverage Flag
# ----------------------------------

demand["Covered"] = (
    demand["Nearest_Store_Distance"]
    <= SERVICE_RADIUS
).astype(int)

# ----------------------------------
# KPIs
# ----------------------------------

coverage_pct = round(
    demand["Covered"].mean() * 100,
    2
)

avg_distance = round(
    demand["Nearest_Store_Distance"].mean(),
    2
)

uncovered = demand[
    demand["Covered"] == 0
]

high_demand_uncovered = uncovered[
    uncovered["Demand_Tier"] == "High"
]

# ----------------------------------
# Save Results
# ----------------------------------

Path("data/processed").mkdir(
    exist_ok=True
)

demand.to_csv(
    "data/processed/coverage_results.csv",
    index=False
)

# ----------------------------------
# Create Map
# ----------------------------------

m = folium.Map(
    location=[12.9716,77.5946],
    zoom_start=11
)

# Existing Stores

for _, row in stores.iterrows():

    folium.Marker(
        location=[
            row["Latitude"],
            row["Longitude"]
        ],
        icon=folium.Icon(
            color="blue",
            icon="home"
        ),
        popup=row["Store_ID"]
    ).add_to(m)

# Demand Points

for _, row in demand.iterrows():

    color = (
        "green"
        if row["Covered"] == 1
        else "red"
    )

    folium.CircleMarker(
        location=[
            row["Latitude"],
            row["Longitude"]
        ],
        radius=5,
        color=color,
        fill=True,
        fill_opacity=0.8,
        popup=(
            f"Area: {row['Area']}<br>"
            f"Demand: {row['Demand_Score']}<br>"
            f"Distance: {round(row['Nearest_Store_Distance'],2)} km"
        )
    ).add_to(m)

# Save Map

Path("maps").mkdir(
    exist_ok=True
)

m.save(
    "maps/coverage_map.html"
)

# ----------------------------------
# Print Insights
# ----------------------------------

print("\nNETWORK COVERAGE ANALYSIS\n")

print(
    f"Coverage Percentage: {coverage_pct}%"
)

print(
    f"Average Distance: {avg_distance} km"
)

print(
    f"Uncovered Demand Points: {len(uncovered)}"
)

print(
    f"High Demand Uncovered Points: {len(high_demand_uncovered)}"
)

print(
    "\nCoverage map saved:"
)

print(
    "maps/coverage_map.html"
)