# Extract from api: coingecko



import requests
import pandas as pd
import os
from datetime import datetime

# STEP 1: EXTRACT - Fetch Top 100 Crypto Prices (CoinGecko API)

# Create raw data folder if missing
os.makedirs("data/raw", exist_ok=True)

# CoinGecko API endpoint for top 100 cryptocurrencies
API_URL = "https://api.coingecko.com/api/v3/coins/markets"

params = {
    "vs_currency": "usd",
    "order": "market_cap_desc",
    "per_page": 100,
    "page": 1,
    "price_change_percentage": "1h,24h,7d"
}

print("Data Fetched from API_URL")

response = requests.get(API_URL, params=params)

if response.status_code != 200:
    raise Exception(f"❌ API request failed with status code {response.status_code}") # raise error if api request fails 

data = response.json()

# Convert JSON → DataFrame
df = pd.DataFrame(data)

# Timestamp for snapshotting
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# Output path
file_path = f"data/raw/crypto_prices_{timestamp}.csv"

# Save CSV
df.to_csv(file_path, index=False)

print("Extraction complete!")
print(f"   {file_path}")
