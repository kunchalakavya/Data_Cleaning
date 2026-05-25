"""
generate_data.py
Generates a realistic but messy raw sales dataset for demonstration.
"""

import pandas as pd
import numpy as np
from faker import Faker

fake = Faker()
np.random.seed(42)
Faker.seed(42)

N = 300

regions = ["North", "South", "East", "West", "NORTH", "south", "EAST", "west"]
categories = ["Electronics", "Clothing", "Food", "electronics", "CLOTHING", None]
statuses = ["Completed", "Pending", "Cancelled", "completed", "PENDING", None]

data = {
    "order_id":   [f"ORD-{i:04d}" for i in range(1, N + 1)],
    "customer_name": [fake.name() for _ in range(N)],
    "email":      [fake.email() if np.random.rand() > 0.05 else None for _ in range(N)],
    "region":     np.random.choice(regions, N).tolist(),
    "category":   np.random.choice(categories, N).tolist(),
    "order_date": pd.date_range("2024-01-01", periods=N, freq="D").strftime("%Y-%m-%d").tolist(),
    "quantity":   [int(q) if np.random.rand() > 0.04 else None for q in np.random.randint(1, 20, N)],
    "unit_price": [round(p, 2) if np.random.rand() > 0.04 else None
                   for p in np.random.uniform(5, 500, N)],
    "status":     np.random.choice(statuses, N).tolist(),
    "sales_rep":  [fake.name() if np.random.rand() > 0.06 else None for _ in range(N)],
}

df = pd.DataFrame(data)

# Inject duplicates
dupes = df.sample(15, random_state=1)
df = pd.concat([df, dupes], ignore_index=True)

# Corrupt some emails
for i in np.random.choice(df.index, 10, replace=False):
    df.at[i, "email"] = "notanemail"

# Add a revenue column with occasional bad strings
df["revenue"] = df.apply(
    lambda r: round(r["quantity"] * r["unit_price"], 2)
    if pd.notna(r["quantity"]) and pd.notna(r["unit_price"]) else None,
    axis=1,
).astype(object)
# Corrupt a few revenue cells
for i in np.random.choice(df.index, 8, replace=False):
    df.at[i, "revenue"] = "N/A"

df.to_csv("raw_sales_data.csv", index=False)
print(f"raw_sales_data.csv created  ({len(df)} rows, {df.shape[1]} columns)")
print(f"  Missing values:\n{df.isnull().sum()[df.isnull().sum() > 0]}")
print(f"  Duplicate rows: {df.duplicated().sum()}")
