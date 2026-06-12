import pandas as pd
import numpy as np
import random
from pathlib import Path

np.random.seed(42)
random.seed(42)

# ----------------------------
# Bangalore Locations
# ----------------------------

locations = {
    "Whitefield": (12.9698, 77.7499),
    "Bellandur": (12.9279, 77.6762),
    "HSR Layout": (12.9116, 77.6474),
    "Koramangala": (12.9352, 77.6245),
    "Indiranagar": (12.9784, 77.6408),
    "Marathahalli": (12.9591, 77.6974),
    "Electronic City": (12.8399, 77.6770),
    "Sarjapur": (12.9077, 77.6960),
    "Hebbal": (13.0358, 77.5970),
    "Yelahanka": (13.1007, 77.5963),
    "KR Puram": (13.0077, 77.6955),
    "Jayanagar": (12.9250, 77.5938)
}

output_path = Path("data/raw")
output_path.mkdir(parents=True, exist_ok=True)

# --------------------------------------------------
# DEMAND POINTS
# --------------------------------------------------

demand_data = []

for i in range(150):

    area = random.choice(list(locations.keys()))
    lat, lon = locations[area]

    demand_data.append([
        f"D{i+1:03d}",
        area,
        lat + np.random.normal(0, 0.01),
        lon + np.random.normal(0, 0.01),
        np.random.randint(20000, 120000),
        np.random.randint(50, 100),
        np.random.randint(40, 100)
    ])

demand_df = pd.DataFrame(
    demand_data,
    columns=[
        "Demand_ID",
        "Area",
        "Latitude",
        "Longitude",
        "Population",
        "Income_Index",
        "Commercial_Index"
    ]
)

# --------------------------------------------------
# EXISTING DARK STORES
# --------------------------------------------------

store_data = []

for i in range(30):

    area = random.choice(list(locations.keys()))
    lat, lon = locations[area]

    store_data.append([
        f"DS{i+1:03d}",
        lat + np.random.normal(0, 0.005),
        lon + np.random.normal(0, 0.005)
    ])

stores_df = pd.DataFrame(
    store_data,
    columns=[
        "Store_ID",
        "Latitude",
        "Longitude"
    ]
)

# --------------------------------------------------
# COMPETITORS
# --------------------------------------------------

competitors = ["Blinkit", "Zepto", "Instamart"]

competitor_data = []

for i in range(50):

    area = random.choice(list(locations.keys()))
    lat, lon = locations[area]

    competitor_data.append([
        random.choice(competitors),
        lat + np.random.normal(0, 0.007),
        lon + np.random.normal(0, 0.007)
    ])

competitor_df = pd.DataFrame(
    competitor_data,
    columns=[
        "Company",
        "Latitude",
        "Longitude"
    ]
)

# --------------------------------------------------
# CANDIDATE SITES
# --------------------------------------------------

candidate_data = []

for i in range(25):

    area = random.choice(list(locations.keys()))
    lat, lon = locations[area]

    candidate_data.append([
        f"C{i+1:03d}",
        area,
        lat + np.random.normal(0, 0.008),
        lon + np.random.normal(0, 0.008)
    ])

candidate_df = pd.DataFrame(
    candidate_data,
    columns=[
        "Site_ID",
        "Area",
        "Latitude",
        "Longitude"
    ]
)

# --------------------------------------------------
# SAVE FILES
# --------------------------------------------------

demand_df.to_csv(output_path / "demand_points.csv", index=False)

stores_df.to_csv(
    output_path / "existing_dark_stores.csv",
    index=False
)

competitor_df.to_csv(
    output_path / "competitors.csv",
    index=False
)

candidate_df.to_csv(
    output_path / "candidate_sites.csv",
    index=False
)

print("\nDatasets Generated Successfully!\n")

print("Demand Points:", len(demand_df))
print("Dark Stores:", len(stores_df))
print("Competitor Stores:", len(competitor_df))
print("Candidate Sites:", len(candidate_df))