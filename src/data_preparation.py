import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from pathlib import Path

# --------------------------
# Load Data
# --------------------------

df = pd.read_csv("data/raw/demand_points.csv")

# --------------------------
# Scale Features
# --------------------------

scaler = MinMaxScaler()

df[
    [
        "Population_Scaled",
        "Income_Scaled",
        "Commercial_Scaled"
    ]
] = scaler.fit_transform(
    df[
        [
            "Population",
            "Income_Index",
            "Commercial_Index"
        ]
    ]
)

# --------------------------
# Demand Score
# --------------------------

df["Demand_Score"] = (
    0.50 * df["Population_Scaled"]
    + 0.30 * df["Income_Scaled"]
    + 0.20 * df["Commercial_Scaled"]
)

# Convert to 0-100 scale

df["Demand_Score"] = (
    df["Demand_Score"] * 100
).round(2)

# --------------------------
# Demand Tier
# --------------------------

df["Demand_Tier"] = pd.cut(
    df["Demand_Score"],
    bins=[0,40,70,100],
    labels=["Low","Medium","High"]
)

# --------------------------
# Save
# --------------------------

output_path = Path(
    "data/processed/demand_scored.csv"
)

df.to_csv(
    output_path,
    index=False
)

print("\nDemand scoring completed.\n")

print(
    df[
        [
            "Area",
            "Demand_Score",
            "Demand_Tier"
        ]
    ].head()
)

print(
    f"\nSaved to: {output_path}"
)