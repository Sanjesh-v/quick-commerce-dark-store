import pandas as pd
from geopy.distance import geodesic
from pathlib import Path
import folium

# ----------------------------------
# Parameters
# ----------------------------------

SERVICE_RADIUS = 3
NUM_NEW_STORES = 5

# ----------------------------------
# Load Data
# ----------------------------------

sites = pd.read_csv(
    "data/processed/site_rankings.csv"
)

demand = pd.read_csv(
    "data/processed/coverage_results.csv"
)

# Only demand not already covered

remaining_demand = demand[
    demand["Covered"] == 0
].copy()

selected_sites = []

# ----------------------------------
# Greedy Selection
# ----------------------------------

for _ in range(NUM_NEW_STORES):

    best_site = None
    best_coverage = -1

    for _, site in sites.iterrows():

        if site["Site_ID"] in [
            s["Site_ID"] for s in selected_sites
        ]:
            continue

        coverage = 0

        for _, demand_point in remaining_demand.iterrows():

            dist = geodesic(
                (
                    site["Latitude"],
                    site["Longitude"]
                ),
                (
                    demand_point["Latitude"],
                    demand_point["Longitude"]
                )
            ).km

            if dist <= SERVICE_RADIUS:
                coverage += demand_point[
                    "Demand_Score"
                ]

        if coverage > best_coverage:
            best_coverage = coverage
            best_site = site

    selected_sites.append(best_site)

    # Remove newly covered demand

    covered_indices = []

    for idx, demand_point in remaining_demand.iterrows():

        dist = geodesic(
            (
                best_site["Latitude"],
                best_site["Longitude"]
            ),
            (
                demand_point["Latitude"],
                demand_point["Longitude"]
            )
        ).km

        if dist <= SERVICE_RADIUS:
            covered_indices.append(idx)

    remaining_demand = remaining_demand.drop(
        covered_indices
    )

# ----------------------------------
# Results
# ----------------------------------

recommendations = pd.DataFrame(
    selected_sites
)

recommendations = recommendations[
    [
        "Site_ID",
        "Area",
        "Latitude",
        "Longitude",
        "Site_Score"
    ]
]

recommendations["Recommendation_Rank"] = range(
    1,
    len(recommendations)+1
)

# ----------------------------------
# Save
# ----------------------------------

Path("reports").mkdir(
    exist_ok=True
)

recommendations.to_csv(
    "reports/final_recommendations.csv",
    index=False
)

# ----------------------------------
# Create Recommendation Map
# ----------------------------------

m = folium.Map(
    location=[12.9716, 77.5946],
    zoom_start=11
)

# Recommended Sites

for _, row in recommendations.iterrows():

    folium.Marker(
        location=[
            row["Latitude"],
            row["Longitude"]
        ],
        popup=(
            f"Rank: {row['Recommendation_Rank']}<br>"
            f"Area: {row['Area']}<br>"
            f"Score: {row['Site_Score']}"
        ),
        icon=folium.Icon(
            color="green",
            icon="star"
        )
    ).add_to(m)

# Uncovered Demand

for _, row in demand.iterrows():

    if row["Covered"] == 0:

        folium.CircleMarker(
            location=[
                row["Latitude"],
                row["Longitude"]
            ],
            radius=4,
            color="red",
            fill=True
        ).add_to(m)

m.save(
    "maps/recommended_sites_map.html"
)

# ----------------------------------
# Summary
# ----------------------------------

print("\nTOP 5 RECOMMENDED DARK STORES\n")

print(
    recommendations[
        [
            "Recommendation_Rank",
            "Area",
            "Site_Score"
        ]
    ]
)

print(
    "\nSaved:"
)

print(
    "reports/final_recommendations.csv"
)

print(
    "maps/recommended_sites_map.html"
)