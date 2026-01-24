"""
Transform step for CoinGecko crypto data

- Reads the most recent raw CSV from data/raw
- Cleans and standardises columns
- Adds a few simple derived metrics
- Writes a timestamped clean file to data/clean
"""

import os
from datetime import datetime
import pandas as pd



# SET PATHS

RAW_FOLDER = "data/raw"
CLEAN_FOLDER = "data/clean"

os.makedirs(CLEAN_FOLDER, exist_ok=True)



# LOAD LATEST RAW FILE

raw_files = [f for f in os.listdir(RAW_FOLDER) if f.endswith(".csv")]

if len(raw_files) == 0:
    raise FileNotFoundError(
        "No raw CSV files found in data/raw. Run extract step first."
    )

raw_files.sort(reverse=True)
latest_file = raw_files[0]
raw_path = os.path.join(RAW_FOLDER, latest_file)

df = pd.read_csv(raw_path)



# BASIC CLEANING


# Drop columns we do not need for analytics
columns_to_drop = [
    "image",
    "fully_diluted_valuation"
]

# "Drop columns if function: columns_to_drop is executed"
df = df.drop(
    columns=[c for c in columns_to_drop if c in df.columns] # used loop
)

# Main Standardize 

# Rename columns to consistent snake_case names 
df = df.rename(
    columns={
        "id": "coin_id",
        "current_price": "price_usd",
        "market_cap": "market_cap",
        "total_volume": "volume_24h",
        "price_change_percentage_24h": "pct_change_24h",
        "price_change_percentage_7d_in_currency": "pct_change_7d"
    }
)


# Ensure expected numeric columns exist
expected_columns = [
    "pct_change_24h",
    "pct_change_7d",
    "volume_24h"
]

for col in expected_columns:       # for loop
    if col not in df.columns:
        df[col] = 0


# Replace missing values with 0 for numerical analysis
df = df.fillna(0)



# FEATURE ENGINEERING

# Convert percentage change into decimal daily return
df["daily_return"] = df["pct_change_24h"] / 100             


# Simple volatility proxy based on recent price movements
df["volatility_score"] = (
    df["pct_change_24h"].abs() + df["pct_change_7d"].abs()
) / 2


# Market dominance (share of total market cap)
total_market_cap = df["market_cap"].sum()         # aggregate with sum

if total_market_cap > 0:                          # if/else statement
    df["market_dominance_pct"] = (
        df["market_cap"] / total_market_cap
    ) * 100
else:
    df["market_dominance_pct"] = 0


# Metadata for auditing
df["transform_timestamp"] = datetime.utcnow().strftime(    # timestamp when the transform step ran
    "%Y-%m-%d %H:%M:%S"
)



# SAVE CLEAN DATA


timestamp = datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S")
clean_file = f"crypto_clean_{timestamp}.csv"
clean_path = os.path.join(CLEAN_FOLDER, clean_file)

df.to_csv(clean_path, index=False)

print(f"Transform complete. Clean file written to: {clean_path}")
print(f"Row count: {len(df)}")
