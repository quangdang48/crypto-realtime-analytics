# Project Context

## Purpose

Build an automated data pipeline that fetches cryptocurrency prices (BTC, ETH, SOL) from public APIs, stores raw data in PostgreSQL, transforms it via dbt into a DuckDB data warehouse for analytical queries (moving averages, volatility, hourly aggregations), and visualizes market trends through a BI dashboard — all orchestrated by Apache Airflow and containerized with Docker.

This is a learning-oriented pet project following a code-first Modern Data Stack approach, designed for a software engineering student transitioning into data engineering.

## Tech Stack

- **Language**: Python 3.11+
- **Source Database (OLTP)**: PostgreSQL 15+ (`postgres:15-alpine`)
- **Data Warehouse (OLAP)**: DuckDB (single-file, local columnar DB)
- **Orchestrator**: Apache Airflow 2.7+ (`apache/airflow:2.7.0`)
- **Transform**: dbt-core 1.7+ with `dbt-duckdb` and `dbt-postgres` adapters
- **Visualization**: Evidence.dev (code-first, Markdown + SQL) or Metabase
- **Infrastructure**: Docker & Docker Compose
- **Key Python libraries**: `requests`, `psycopg2-binary`, `duckdb`, `pandas`, `python-dotenv`

## Project Conventions

### Code Style

- Python scripts use **snake_case** for functions, variables, and file names
- SQL files use **snake_case** for tables, columns, and model names
- Environment variables use **UPPER_SNAKE_CASE** (e.g., `DB_NAME`, `DB_USERNAME`)
- Configuration lives in `.env` files, loaded via `python-dotenv`; secrets are never committed

### Naming Conventions

| Pattern      | Example             | Used For                     |
| ------------ | ------------------- | ---------------------------- |
| `stg_*`      | `stg_crypto_prices` | dbt staging models           |
| `fct_*`      | `fct_price_hourly`  | dbt fact tables (marts)      |
| `dim_*`      | `dim_coins`         | dbt dimension tables (marts) |
| `staging_*`  | `staging_crypto`    | Raw PostgreSQL tables        |
| `*_pipeline` | `crypto_pipeline`   | Airflow DAG IDs              |

### Architecture Patterns

- **ELT pattern**: Extract raw data into PostgreSQL, then transform inside the warehouse (DuckDB) using dbt
- **Separation of concerns**: Extraction scripts (`scripts/`) are independent of DAG definitions (`dags/`); Airflow imports and calls them
- **dbt layering**: staging → intermediate (optional) → marts
- **Containerized services**: Every component runs in Docker; `docker-compose.yml` is the single entry point
- **Raw data preservation**: The `raw_json` JSONB column in `staging_crypto` stores the full API response for future flexibility

### Testing Strategy

- **dbt tests**: `not_null`, `unique`, `accepted_values` on staging and mart models via `schema.yml`
- **Manual verification**: Query PostgreSQL to confirm data ingestion before automating
- **Airflow UI**: Monitor DAG runs, task logs, and retry status via http://localhost:8080

### Git Workflow

- **Main branch**: `main`
- **Commit style**: Descriptive messages (e.g., `"Add extraction script for CoinGecko API"`)
- **`.gitignore`**: Excludes `.env`, `logs/`, `__pycache__/`, `*.duckdb`, `dbt/target/`, `dbt/dbt_packages/`

## Domain Context

- **Cryptocurrency market data**: Prices, 24h trading volume, market cap, and price change percentages for BTC, ETH, and SOL
- **Key analytics computed by dbt**:
  - **Moving Average**: 1-hour rolling average price per coin
  - **Volatility**: Spread between highest and lowest prices per time window
  - **Hourly aggregation**: `fct_price_hourly` for trend analysis
- **Data freshness**: Pipeline runs every 5 minutes (`*/5 * * * *` cron in Airflow)
- **Timezone handling**: All timestamps stored as `TIMESTAMP WITH TIME ZONE`; dbt models normalize to UTC

## Important Constraints

- **Free-tier APIs only**: CoinGecko and Binance public endpoints (no API key required for basic usage); rate limits apply
- **Local-only deployment**: Everything runs on a single developer machine via Docker Compose; no cloud infrastructure
- **DuckDB scale**: Suitable for datasets under ~100 GB; sufficient for this project's scope
- **Learning project**: Prioritize clarity and standard patterns over optimization

## External Dependencies

- **CoinGecko API**: `GET /api/v3/coins/markets` — primary data source for coin prices and market data
- **Binance Public API**: Alternative/supplementary data source (no auth required)
- **Docker Hub images**: `postgres:15-alpine`, `apache/airflow:2.7.0-python3.11`, `metabase/metabase` (optional)

## Key Ports

| Service                 | Port |
| ----------------------- | ---- |
| PostgreSQL              | 5432 |
| Airflow Web UI          | 8080 |
| Evidence.dev / Metabase | 3000 |
