import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import folium
from pathlib import Path

# ----------------------------------
# Load Data
# ----------------------------------

df = pd.read_csv(
    "data/processed/demand_scored.csv"
)

# ----------------------------------
# Features for Clustering
# ----------------------------------

X = df[
    [
        "Latitude",
        "Longitude",
        "Demand_Score"
    ]
]

# ----------------------------------
# Standardize
# ----------------------------------

scaler = StandardScaler()

X_scaled = scaler.fit_transform(X)

# ----------------------------------
# KMeans
# ----------------------------------

kmeans = KMeans(
    n_clusters=6,
    random_state=42,
    n_init=10
)

df["Cluster"] = kmeans.fit_predict(
    X_scaled
)

# ----------------------------------
# Cluster Summary
# ----------------------------------

cluster_summary = (
    df.groupby("Cluster")
    .agg(
        Demand_Points=("Demand_ID","count"),
        Avg_Demand=("Demand_Score","mean")
    )
    .reset_index()
)

cluster_summary["Avg_Demand"] = (
    cluster_summary["Avg_Demand"]
    .round(2)
)

print("\nCLUSTER SUMMARY\n")
print(cluster_summary)

# ----------------------------------
# Save Dataset
# ----------------------------------

df.to_csv(
    "data/processed/clustered_demand.csv",
    index=False
)

# ----------------------------------
# Create Map
# ----------------------------------

cluster_colors = {
    0: "red",
    1: "blue",
    2: "green",
    3: "purple",
    4: "orange",
    5: "black"
}

m = folium.Map(
    location=[12.9716,77.5946],
    zoom_start=11
)

# ----------------------------------
# Demand Points
# ----------------------------------

for _, row in df.iterrows():

    folium.CircleMarker(
        location=[
            row["Latitude"],
            row["Longitude"]
        ],
        radius=5,
        color=cluster_colors[row["Cluster"]],
        fill=True,
        fill_opacity=0.7,
        popup=(
            f"Area: {row['Area']}<br>"
            f"Cluster: {row['Cluster']}<br>"
            f"Demand: {row['Demand_Score']}"
        )
    ).add_to(m)

# ----------------------------------
# Cluster Centroids
# ----------------------------------

centroids = (
    df.groupby("Cluster")
    [["Latitude","Longitude"]]
    .mean()
    .reset_index()
)

for _, row in centroids.iterrows():

    folium.Marker(
        location=[
            row["Latitude"],
            row["Longitude"]
        ],
        popup=f"Cluster {int(row['Cluster'])}",
        icon=folium.Icon(
            icon="home"
        )
    ).add_to(m)

# ----------------------------------
# Save Map
# ----------------------------------

Path("maps").mkdir(
    exist_ok=True
)

m.save(
    "maps/cluster_map.html"
)

print(
    "\nCluster map saved:"
)

print(
    "maps/cluster_map.html"
)