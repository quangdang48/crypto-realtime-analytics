# Project Structure

Detailed explanation of the directory layout and the purpose of each file/folder.

---

```
crypto-realtime-analytics-pipeline/
│
├── README.md                        # Project overview and quick start guide
├── docker-compose.yml               # Defines all services (Postgres, Airflow, etc.)
├── requirements.txt                 # Python dependencies for the project
├── .env                             # Environment variables (DB credentials, API keys)
├── .env.example                     # Template for .env (committed to git)
├── .gitignore                       # Files excluded from version control
│
├── dags/                            # Airflow DAG definitions
│   ├── crypto_pipeline.py           # Main DAG: extract crypto data every 5 min
│   └── hello_world.py               # Test DAG for learning Airflow basics
│
├── scripts/                         # Python scripts for data extraction
│   ├── extract_crypto.py            # Fetches data from CoinGecko/Binance API
│   └── __init__.py                  # Makes scripts importable as a module
│
├── sql/                             # Raw SQL scripts
│   └── init.sql                     # Creates staging_crypto table (run on first setup)
│
├── dbt/                             # dbt project for data transformations
│   ├── dbt_project.yml              # dbt project configuration
│   ├── profiles.yml                 # Database connection profiles
│   ├── packages.yml                 # dbt package dependencies (optional)
│   │
│   ├── models/
│   │   ├── staging/                 # Staging layer — light cleaning of raw data
│   │   │   ├── stg_crypto_prices.sql
│   │   │   └── schema.yml           # Column descriptions and tests
│   │   │
│   │   ├── intermediate/            # Intermediate layer — joins, business logic (optional)
│   │   │
│   │   └── marts/                   # Mart layer — final analytical tables
│   │       ├── fct_price_hourly.sql      # Hourly price aggregation
│   │       ├── fct_moving_average.sql    # 1-hour rolling average per coin
│   │       ├── fct_volatility.sql        # Price volatility (high-low spread)
│   │       ├── dim_coins.sql             # Coin dimension table
│   │       └── schema.yml               # Column descriptions and tests
│   │
│   ├── macros/                      # Reusable SQL macros (optional)
│   ├── seeds/                       # Static CSV data (optional)
│   ├── snapshots/                   # Slowly changing dimension snapshots (optional)
│   └── tests/                       # Custom data quality tests (optional)
│
├── docker/                          # Custom Dockerfiles (if needed)
│   └── airflow/
│       └── Dockerfile               # Extends base Airflow image with project deps
│
├── docs/                            # Project documentation
│   ├── architecture.md              # System design and data flow diagrams
│   ├── tech-stack.md                # Technology choices and rationale
│   ├── roadmap.md                   # Week-by-week implementation plan
│   └── project-structure.md         # This file
│
└── evidence/                        # Evidence.dev dashboard project (optional)
    ├── pages/
    │   └── index.md                 # Dashboard page with SQL + Markdown
    └── evidence.plugins.yaml
```

---

## Directory Details

### `dags/`

Contains Airflow DAG (Directed Acyclic Graph) files. Each `.py` file defines a workflow that Airflow discovers and schedules automatically. The `dags/` folder is mounted into the Airflow container.

### `scripts/`

Python scripts that perform the actual data extraction work. These are called by Airflow tasks. Keep extraction logic here, separate from DAG definitions, for testability and reusability.

### `sql/`

Raw SQL files for database initialization. `init.sql` is executed once to set up the PostgreSQL schema. Can be auto-run via Docker Compose volume mount to `/docker-entrypoint-initdb.d/`.

### `dbt/`

The dbt project that transforms raw staging data into analytical models inside DuckDB. Follows the standard dbt layer convention:

- **Staging** → 1:1 with source tables, renamed/retyped columns
- **Intermediate** → Business logic joins (optional for this project)
- **Marts** → Final fact and dimension tables consumed by dashboards

### `docker/`

Custom Dockerfiles when the base images need modification. For example, the Airflow Dockerfile installs additional Python packages (`psycopg2`, `requests`, `duckdb`) on top of the base Airflow image.

### `docs/`

All project documentation in Markdown format. Designed to be readable on GitHub or any Markdown viewer.

### `evidence/`

Optional Evidence.dev project for creating dashboards using Markdown + SQL. Each `.md` page can contain SQL queries that auto-render as charts.

---

## Key Configuration Files

| File                  | Purpose                                                             |
| --------------------- | ------------------------------------------------------------------- |
| `docker-compose.yml`  | Defines services, networks, volumes, environment variables          |
| `.env`                | Stores sensitive config (DB passwords, API keys) — **never commit** |
| `.env.example`        | Template showing required variables — safe to commit                |
| `requirements.txt`    | Python dependencies installed in Airflow container                  |
| `dbt/dbt_project.yml` | dbt project name, version, model paths                              |
| `dbt/profiles.yml`    | DuckDB/PostgreSQL connection settings for dbt                       |

---

## Naming Conventions

| Pattern      | Example             | Used For                     |
| ------------ | ------------------- | ---------------------------- |
| `stg_*`      | `stg_crypto_prices` | Staging models (dbt)         |
| `fct_*`      | `fct_price_hourly`  | Fact tables (dbt marts)      |
| `dim_*`      | `dim_coins`         | Dimension tables (dbt marts) |
| `staging_*`  | `staging_crypto`    | Raw PostgreSQL tables        |
| `*_pipeline` | `crypto_pipeline`   | Airflow DAG names            |
