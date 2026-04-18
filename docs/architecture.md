# Architecture

## System Overview

The Crypto Real-time Analytics Pipeline follows a classic **ELT (Extract, Load, Transform)** pattern with four distinct layers:

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        ORCHESTRATION LAYER                              │
│                       (Apache Airflow)                                  │
│   ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐           │
│   │  Task 1  │───▶│  Task 2  │───▶│  Task 3  │───▶│  Task 4  │          │
│   │ Extract  │    │  Load    │    │Transform │    │  Notify  │          │
│   └─────────┘    └─────────┘    └─────────┘    └─────────┘           │
└─────────────────────────────────────────────────────────────────────────┘
       │                 │                │                │
       ▼                 ▼                ▼                ▼
┌──────────┐     ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ External │     │  PostgreSQL  │  │    DuckDB    │  │  Evidence.dev│
│   APIs   │     │  (Staging)   │  │ (Warehouse)  │  │  (Dashboard) │
└──────────┘     └──────────────┘  └──────────────┘  └──────────────┘
```

## Data Flow

### Step 1: Extract (Data Ingestion)

```
CoinGecko API / Binance API
        │
        ▼
  Python Script (requests)
        │
        ▼
  Raw JSON Response
        │
        ▼
  PostgreSQL: staging_crypto
```

- **Source**: CoinGecko or Binance Public API (no API key required for basic endpoints)
- **Frequency**: Every 5 minutes via Airflow scheduler
- **Target coins**: BTC (Bitcoin), ETH (Ethereum), SOL (Solana)
- **Data captured**:
  - Current price (USD)
  - 24h trading volume
  - Market cap
  - Price change percentage (24h)
  - Timestamp of fetch

### Step 2: Load (Staging)

```
PostgreSQL (staging_crypto)
        │
        ├── id (SERIAL PRIMARY KEY)
        ├── coin_id (VARCHAR)
        ├── symbol (VARCHAR)
        ├── price_usd (DECIMAL)
        ├── volume_24h (DECIMAL)
        ├── market_cap (DECIMAL)
        ├── price_change_24h (DECIMAL)
        ├── fetched_at (TIMESTAMP WITH TIME ZONE)
        └── raw_json (JSONB)
```

- Raw data lands in PostgreSQL as-is (no transformation)
- The `raw_json` column preserves the full API response for future use
- PostgreSQL acts as the **single source of truth** for raw data

### Step 3: Transform (dbt Models)

```
PostgreSQL (staging)  ──▶  dbt  ──▶  DuckDB (warehouse)
                            │
                  ┌─────────┼──────────┐
                  ▼         ▼          ▼
            stg_crypto   moving_avg   volatility
            (cleaned)    (1h window)  (high-low)
```

**Staging Models** (`models/staging/`):

- `stg_crypto_prices` — Cleaned and typed data from raw staging table

**Mart Models** (`models/marts/`):

- `fct_price_hourly` — Hourly aggregated price data
- `fct_moving_average` — 1-hour moving average per coin
- `fct_volatility` — Price volatility (high-low spread) per time window
- `dim_coins` — Coin dimension table (id, name, symbol)

### Step 4: Visualize (BI Layer)

```
DuckDB (warehouse)
        │
        ▼
  Evidence.dev / Metabase
        │
        ├── Price trend line chart (BTC, ETH, SOL)
        ├── Volume bar chart (24h)
        ├── Moving average overlay
        └── Volatility heatmap
```

## Infrastructure (Docker Compose)

```
docker-compose.yml
├── postgres         (Port 5432)
├── airflow-webserver (Port 8080)
├── airflow-scheduler
├── airflow-init     (One-time setup)
└── evidence         (Port 3000) [optional]
```

All services run in Docker containers, connected via a shared Docker network. Volumes persist data across container restarts.

## Key Design Decisions

| Decision         | Choice              | Rationale                                                 |
| ---------------- | ------------------- | --------------------------------------------------------- |
| OLTP Database    | PostgreSQL          | Industry standard, great JSON support, Docker-friendly    |
| OLAP Database    | DuckDB              | Lightweight, runs locally, columnar storage for analytics |
| Orchestrator     | Apache Airflow      | Most widely used in industry, great learning value        |
| Transform tool   | dbt                 | SQL-first approach, version-controlled transformations    |
| API source       | CoinGecko / Binance | Free tier, reliable, well-documented                      |
| Containerization | Docker Compose      | Single command to spin up entire environment              |
