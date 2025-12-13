# Crypto Market Data Engineering Pipeline (Microsoft Fabric)

## 📌 Project Overview

This project is an end-to-end **data engineering pipeline** that ingests cryptocurrency market data, processes it using a **Lakehouse architecture**, and exposes it for analytics through **Power BI**.

The goal of this project is to demonstrate **core data engineering skills** (ingestion, transformation, validation, storage, and analytics enablement) using modern Microsoft tools, rather than advanced financial analysis.

---


## 🧠 Design Decisions & Tradeoffs

* **Fabric Lakehouse** chosen to demonstrate modern Microsoft analytics stack
* **CSV snapshots** used instead of streaming for simplicity and reproducibility
* **Minimal DAX** to keep focus on data engineering rather than analytics
* **No orchestration tool** in this project (handled in a separate ADF project)


## 🏗️ Architecture

**High-level flow:**

1. **Extract** – Python script pulls Top 100 cryptocurrency market data (prices, market cap, volume, etc.) from a public API.
2. **Bronze Layer** – Raw CSV files stored in Fabric Lakehouse (immutable snapshots).
3. **Silver Layer** – Cleaned and validated Delta table (schema enforced, basic quality checks).
4. **Semantic Layer** – Fabric Lakehouse table exposed to Power BI.
5. **Visualization** – Power BI dashboard for exploration and monitoring.

```
API / CSV
   ↓
Bronze (Raw CSV)
   ↓
Silver (Clean Delta Table)
   ↓
Power BI Semantic Model
   ↓
Dashboard
```

---

## 🛠️ Tech Stack

* **Python** – data extraction and transformation
* **pandas** – data cleaning and validation
* **Microsoft Fabric** – Lakehouse, Delta tables, SQL endpoint
* **OneLake** – unified storage
* **Power BI** – semantic model and dashboard
* **Git & GitHub** – version control

---

## 📂 Repository Structure

```
crypto-fabric-pipeline/
│
├── data/
│   ├── raw/              # Bronze layer CSV snapshots
│   └── clean/            # Cleaned CSV outputs (Silver input)
│
├── src/
│   ├── extract.py        # Pulls crypto data
│   └── transform.py     # Cleans & validates data
│
├── powerbi/
│   └── dashboard.png    # Dashboard screenshot
│
├── README.md
└── .gitignore
```

---

## 🔄 Data Pipeline Steps

### 1️⃣ Extract

* Fetches Top 100 cryptocurrencies
* Stores timestamped raw CSV files
* Ensures reproducibility and auditability

### 2️⃣ Transform (Silver Layer)

* Removes invalid or missing values
* Normalizes column names
* Enforces schema consistency
* Outputs clean dataset for analytics

### 3️⃣ Load (Fabric Lakehouse)

* Clean data loaded into Fabric Lakehouse
* Stored as Delta tables
* Queryable via SQL Endpoint

### 4️⃣ Analytics & Visualization

* Lakehouse table connected to Power BI via OneLake
* No local dashboards or custom APIs required
* Visuals summarize trends and market movements

---

## 📊 Power BI Dashboard

The dashboard focuses on **operational visibility**, not financial prediction:

* Top 10 cryptocurrencies by market cap
* Daily price change (% gainers / losers)
* Market dominance overview
* Price trends over time
* Volume comparison table
* Interactive filters (date, coin)

> The visuals intentionally remain simple to highlight data reliability and pipeline correctness.

---

## ✅ Data Quality Checks

Basic checks applied during transformation:

* No negative prices
* Required fields not null
* Duplicate rows removed
* Numeric columns validated

Failures are logged during processing.

---

## 🚀 How to Run

1. Create a virtual environment
2. Install dependencies
3. Run extraction script
4. Run transformation script
5. Upload cleaned data to Fabric Lakehouse
6. Refresh Power BI semantic model
