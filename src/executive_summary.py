import pandas as pd
from geopy.distance import geodesic

SERVICE_RADIUS = 3

# ----------------------------------
# Load Data
# ----------------------------------

coverage = pd.read_csv(
    "data/processed/coverage_results.csv"
)

recommendations = pd.read_csv(
    "reports/final_recommendations.csv"
)

# ----------------------------------
# Current Network KPIs
# ----------------------------------

current_coverage = round(
    coverage["Covered"].mean() * 100,
    2
)

uncovered_demand = len(
    coverage[coverage["Covered"] == 0]
)

high_demand_uncovered = len(
    coverage[
        (coverage["Covered"] == 0)
        &
        (coverage["Demand_Tier"] == "High")
    ]
)

avg_distance = round(
    coverage["Nearest_Store_Distance"].mean(),
    2
)

# ----------------------------------
# Simulate Expansion
# ----------------------------------

expanded = coverage.copy()

for idx, demand_point in expanded.iterrows():

    if demand_point["Covered"] == 1:
        continue

    for _, site in recommendations.iterrows():

        dist = geodesic(
            (
                demand_point["Latitude"],
                demand_point["Longitude"]
            ),
            (
                site["Latitude"],
                site["Longitude"]
            )
        ).km

        if dist <= SERVICE_RADIUS:
            expanded.loc[idx, "Covered"] = 1
            break

# ----------------------------------
# Expanded Coverage
# ----------------------------------

expanded_coverage = round(
    expanded["Covered"].mean() * 100,
    2
)

coverage_improvement = round(
    expanded_coverage - current_coverage,
    2
)

# ----------------------------------
# KPI Table
# ----------------------------------

summary = pd.DataFrame({
    "Metric": [
        "Current Coverage %",
        "Expanded Coverage %",
        "Coverage Improvement %",
        "Average Distance (km)",
        "Uncovered Demand Points",
        "High Demand Uncovered"
    ],
    "Value": [
        current_coverage,
        expanded_coverage,
        coverage_improvement,
        avg_distance,
        uncovered_demand,
        high_demand_uncovered
    ]
})

summary.to_csv(
    "reports/executive_summary.csv",
    index=False
)

print("\nEXECUTIVE SUMMARY\n")
print(summary)

print(
    "\nSaved: reports/executive_summary.csv"
)