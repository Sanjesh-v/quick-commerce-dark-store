import pandas as pd
import numpy as np
from geopy.distance import geodesic
from sklearn.preprocessing import MinMaxScaler

# --------------------------
# Load Data
# --------------------------

candidates = pd.read_csv(
    "data/raw/candidate_sites.csv"
)

demand = pd.read_csv(
    "data/processed/coverage_results.csv"
)

competitors = pd.read_csv(
    "data/raw/competitors.csv"
)

# --------------------------
# Functions
# --------------------------

def avg_demand_nearby(lat, lon, radius=3):

    nearby = []

    for _, row in demand.iterrows():

        dist = geodesic(
            (lat, lon),
            (row["Latitude"], row["Longitude"])
        ).km

        if dist <= radius:
            nearby.append(row["Demand_Score"])

    return np.mean(nearby) if nearby else 0


def population_nearby(lat, lon, radius=3):

    nearby = []

    for _, row in demand.iterrows():

        dist = geodesic(
            (lat, lon),
            (row["Latitude"], row["Longitude"])
        ).km

        if dist <= radius:
            nearby.append(row["Population"])

    return np.sum(nearby)


def competition_gap(lat, lon, radius=3):

    count = 0

    for _, row in competitors.iterrows():

        dist = geodesic(
            (lat, lon),
            (row["Latitude"], row["Longitude"])
        ).km

        if dist <= radius:
            count += 1

    return count

# --------------------------
# Feature Creation
# --------------------------

candidates["Demand_Potential"] = candidates.apply(
    lambda x: avg_demand_nearby(
        x["Latitude"],
        x["Longitude"]
    ),
    axis=1
)

candidates["Population_Potential"] = candidates.apply(
    lambda x: population_nearby(
        x["Latitude"],
        x["Longitude"]
    ),
    axis=1
)

candidates["Competition_Count"] = candidates.apply(
    lambda x: competition_gap(
        x["Latitude"],
        x["Longitude"]
    ),
    axis=1
)

# --------------------------
# Simulated Variables
# --------------------------

np.random.seed(42)

candidates["Accessibility"] = np.random.randint(
    60,
    100,
    len(candidates)
)

candidates["Rent_Proxy"] = np.random.randint(
    50,
    100,
    len(candidates)
)

# --------------------------
# Scale Features
# --------------------------

scaler = MinMaxScaler()

candidates[
    [
        "Demand_Scaled",
        "Population_Scaled",
        "Competition_Scaled",
        "Accessibility_Scaled",
        "Rent_Scaled"
    ]
] = scaler.fit_transform(
    candidates[
        [
            "Demand_Potential",
            "Population_Potential",
            "Competition_Count",
            "Accessibility",
            "Rent_Proxy"
        ]
    ]
)

# Reverse competition
candidates["Competition_Gap"] = (
    1 - candidates["Competition_Scaled"]
)

# --------------------------
# Final Site Score
# --------------------------

candidates["Site_Score"] = (
      0.35 * candidates["Demand_Scaled"]
    + 0.25 * candidates["Population_Scaled"]
    + 0.20 * candidates["Competition_Gap"]
    + 0.10 * candidates["Accessibility_Scaled"]
    + 0.10 * candidates["Rent_Scaled"]
)

candidates["Site_Score"] = (
    candidates["Site_Score"] * 100
).round(2)

# --------------------------
# Ranking
# --------------------------

rankings = candidates.sort_values(
    "Site_Score",
    ascending=False
)

rankings["Rank"] = range(
    1,
    len(rankings) + 1
)

# --------------------------
# Save
# --------------------------

rankings.to_csv(
    "data/processed/site_rankings.csv",
    index=False
)

print("\nTOP 10 SITES\n")

print(
    rankings[
        ["Rank","Site_ID","Area","Site_Score"]
    ].head(10)
)

print(
    "\nSaved:"
)

print(
    "data/processed/site_rankings.csv"
)