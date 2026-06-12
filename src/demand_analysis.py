import pandas as pd
import folium
from folium.plugins import HeatMap
from pathlib import Path

# ----------------------------------
# Load Data
# ----------------------------------

df = pd.read_csv(
    "data/processed/demand_scored.csv"
)

# ----------------------------------
# Area Level Summary
# ----------------------------------

area_summary = (
    df.groupby("Area")
    .agg(
        Demand_Points=("Demand_ID", "count"),
        Avg_Demand=("Demand_Score", "mean"),
        Population=("Population", "sum")
    )
    .reset_index()
)

area_summary["Avg_Demand"] = (
    area_summary["Avg_Demand"]
    .round(2)
)

area_summary = area_summary.sort_values(
    "Avg_Demand",
    ascending=False
)

# ----------------------------------
# Save Summary
# ----------------------------------

area_summary.to_csv(
    "data/processed/area_demand_summary.csv",
    index=False
)

# ----------------------------------
# Bangalore Base Map
# ----------------------------------

m = folium.Map(
    location=[12.9716, 77.5946],
    zoom_start=11
)

# ----------------------------------
# Heatmap Layer
# ----------------------------------

heat_data = [
    [
        row["Latitude"],
        row["Longitude"],
        row["Demand_Score"]
    ]
    for _, row in df.iterrows()
]

HeatMap(
    heat_data,
    radius=20
).add_to(m)

# ----------------------------------
# Demand Points Layer
# ----------------------------------

for _, row in df.iterrows():

    folium.CircleMarker(
        location=[
            row["Latitude"],
            row["Longitude"]
        ],
        radius=4,
        popup=(
            f"Area: {row['Area']}<br>"
            f"Demand Score: {row['Demand_Score']}"
        ),
        fill=True
    ).add_to(m)

# ----------------------------------
# Save Map
# ----------------------------------

Path("maps").mkdir(
    exist_ok=True
)

m.save(
    "maps/demand_heatmap.html"
)

# ----------------------------------
# Insights
# ----------------------------------

print("\nTOP 10 DEMAND AREAS\n")

print(
    area_summary[
        ["Area", "Avg_Demand"]
    ].head(10)
)

print(
    "\nAverage Demand Score:",
    round(
        df["Demand_Score"].mean(),
        2
    )
)

print(
    "\nHigh Demand Markets:",
    len(
        df[
            df["Demand_Tier"] == "High"
        ]
    )
)

print(
    "\nHeatmap Saved:"
)

print(
    "maps/demand_heatmap.html"
)