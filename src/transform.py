# Transform data pulled from coingecko

import pandas as pd
import os
from datetime import datetime

print("🚀 Starting crypto transform step...")

# ============================================================
# CREATE CLEAN FOLDER
# ============================================================
os.makedirs("data/clean", exist_ok=True)
print("📁 Ensured data/clean/ exists.")

# ============================================================
# FIND LATEST RAW FILE
# ============================================================
raw_folder = "data/raw"
raw_files = sorted(
    [f for f in os.listdir(raw_folder) if f.endswith(".csv")],
    reverse=True
)

if not raw_files:
    raise Exception("❌ No raw CSV found in data/raw. Run extract.py first.")

latest_file = raw_files[0]
raw_path = os.path.join(raw_folder, latest_file)

print(f"🔄 Loading latest raw file: {latest_file}")

df = pd.read_csv(raw_path)
print("📥 Raw file loaded successfully.")
print(f"📊 Columns found: {df.columns.tolist()}")

# ============================================================
# CLEANING
# ============================================================
print("🧹 Cleaning data...")

# Drop columns if they exist
columns_to_drop = ["image", "fully_diluted_valuation"]
df = df.drop(columns=[c for c in columns_to_drop if c in df.columns], errors="ignore")

# Safe renaming
rename_map = {
    "id": "coin_id",
    "symbol": "symbol",
    "name": "name",
    "current_price": "price_usd",
    "market_cap": "market_cap",
    "total_volume": "volume_24h",
    "price_change_percentage_24h": "pct_change_24h",
    "price_change_percentage_7d_in_currency": "pct_change_7d",
}

df = df.rename(columns=rename_map)

# Add missing columns if API did not return them
for col in ["pct_change_24h", "pct_change_7d", "volume_24h"]:
    if col not in df:
        df[col] = 0

df = df.fillna(0)
print("🧽 Missing values filled.")

# ============================================================
# FEATURE ENGINEERING
# ============================================================
print("📐 Feature engineering...")

# Daily return
df["daily_return"] = df["pct_change_24h"] / 100

# Volatility score
df["volatility_score"] = (df["pct_change_24h"].abs() + df["pct_change_7d"].abs()) / 2

# Market dominance
total_market_cap = df["market_cap"].sum() if "market_cap" in df else 1
df["market_dominance_pct"] = (df["market_cap"] / total_market_cap) * 100

df["transform_timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

print("✨ Feature engineering complete.")

# ============================================================
# SAVE CLEANED OUTPUT
# ============================================================
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
clean_path = f"data/clean/crypto_clean_{timestamp}.csv"

df.to_csv(clean_path, index=False)

print(f"✅ Transform complete! Saved cleaned file:")
print(f"   {clean_path}")
print(f"📈 Total rows: {len(df)}")
