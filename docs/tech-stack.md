# Tech Stack

## Overview

This project uses a **Modern Data Stack** approach with code-first tools, chosen for learning real-world data engineering skills and leveraging existing backend development experience (Java/NestJS, Docker).

---

## Core Language: Python

| Aspect                   | Detail                                                                          |
| ------------------------ | ------------------------------------------------------------------------------- |
| **Version**              | 3.11+                                                                           |
| **Why Python**           | De facto standard for data engineering; vast ecosystem of data libraries        |
| **Key Libraries**        | `requests`, `psycopg2`, `duckdb`, `pandas`                                      |
| **Transition from Java** | Similar OOP concepts; much less boilerplate; dynamic typing speeds up scripting |

### Key Python Libraries

```
requests        — HTTP client for API calls
psycopg2        — PostgreSQL adapter
duckdb          — DuckDB Python client
pandas          — Data manipulation (optional, for complex transforms)
python-dotenv   — Environment variable management
```

---

## Source Database: PostgreSQL (OLTP)

| Aspect             | Detail                                                            |
| ------------------ | ----------------------------------------------------------------- |
| **Role**           | Operational/transactional database — stores raw ingested data     |
| **Version**        | 15+                                                               |
| **Docker Image**   | `postgres:15-alpine`                                              |
| **Port**           | 5432                                                              |
| **Why PostgreSQL** | Industry standard RDBMS, excellent JSONB support, Docker-friendly |

### Key Features Used

- **JSONB columns** — Store raw API responses for flexible querying
- **Timestamps with timezone** — Proper time handling for global data
- **Serial primary keys** — Auto-incrementing IDs for staging records

---

## Data Warehouse: DuckDB (OLAP)

| Aspect          | Detail                                                                                                                   |
| --------------- | ------------------------------------------------------------------------------------------------------------------------ |
| **Role**        | Analytical database — optimized for read-heavy queries and aggregations                                                  |
| **Why DuckDB**  | Runs locally (no cloud needed), columnar storage, SQL-compatible, comparable to BigQuery/Snowflake for small-medium data |
| **File**        | `warehouse.duckdb` (single file)                                                                                         |
| **Alternative** | Google BigQuery (free tier: 1 TB queries/month)                                                                          |

### DuckDB vs Traditional Warehouses

| Feature     | DuckDB                   | BigQuery            | Snowflake   |
| ----------- | ------------------------ | ------------------- | ----------- |
| Cost        | Free                     | Free tier           | Paid        |
| Setup       | Zero config              | Cloud setup         | Cloud setup |
| Performance | Great for < 100GB        | Unlimited           | Unlimited   |
| Learning    | Perfect for pet projects | Good for production | Enterprise  |

---

## Orchestrator: Apache Airflow

| Aspect           | Detail                                                                |
| ---------------- | --------------------------------------------------------------------- |
| **Role**         | Workflow scheduler — triggers ETL tasks on a defined schedule         |
| **Version**      | 2.7+                                                                  |
| **Docker Image** | `apache/airflow:2.7.0`                                                |
| **Web UI Port**  | 8080                                                                  |
| **Schedule**     | Every 5 minutes (`*/5 * * * *`)                                       |
| **Why Airflow**  | Most widely adopted orchestrator in the industry; strong resume value |

### Core Concepts

- **DAG** (Directed Acyclic Graph) — Defines the workflow
- **Task** — A single unit of work (e.g., run a Python script)
- **Operator** — Template for a task (PythonOperator, BashOperator)
- **Schedule Interval** — How often the DAG runs

### Alternative: Mage.ai

- More modern UI, easier to get started
- Less industry adoption than Airflow
- Good option if Airflow feels too complex initially

---

## Transform Tool: dbt (data build tool)

| Aspect      | Detail                                                             |
| ----------- | ------------------------------------------------------------------ |
| **Role**    | SQL-based data transformation inside the warehouse                 |
| **Version** | dbt-core 1.7+ with `dbt-duckdb` adapter                            |
| **Why dbt** | Version-controlled SQL, built-in testing, documentation generation |

### dbt Model Layers

```
models/
├── staging/           # 1:1 mapping with source tables, light cleaning
│   └── stg_crypto_prices.sql
├── intermediate/      # Business logic joins and calculations (optional)
└── marts/             # Final analytical tables
    ├── fct_price_hourly.sql
    ├── fct_moving_average.sql
    └── fct_volatility.sql
```

### Key dbt Features Used

- **Models** — SQL SELECT statements that create tables/views
- **Sources** — Define and document raw data connections
- **Tests** — Validate data quality (not_null, unique, accepted_values)
- **Documentation** — Auto-generated data lineage graphs

---

## Visualization: Evidence.dev / Metabase

### Option A: Evidence.dev (Recommended for learning)

| Aspect       | Detail                                                |
| ------------ | ----------------------------------------------------- |
| **Approach** | Markdown + SQL → auto-generated charts                |
| **Port**     | 3000                                                  |
| **Why**      | Code-first BI tool, version-controllable, lightweight |

### Option B: Metabase

| Aspect           | Detail                                       |
| ---------------- | -------------------------------------------- |
| **Approach**     | GUI-based dashboarding tool                  |
| **Docker Image** | `metabase/metabase`                          |
| **Port**         | 3000                                         |
| **Why**          | More traditional BI, drag-and-drop interface |

---

## Infrastructure: Docker & Docker Compose

| Aspect             | Detail                                                                            |
| ------------------ | --------------------------------------------------------------------------------- |
| **Docker**         | Containerizes each service independently                                          |
| **Docker Compose** | Defines and runs the multi-container environment                                  |
| **Why**            | One command (`docker-compose up`) starts everything; reproducible across machines |

### Services Defined in `docker-compose.yml`

```yaml
services:
  postgres: # Source database
  airflow-init: # One-time Airflow DB initialization
  airflow-webserver: # Airflow UI
  airflow-scheduler: # Airflow task executor
  evidence: # BI dashboard (optional)
```

---

## Full Dependency List

### Python (`requirements.txt`)

```
requests>=2.31.0
psycopg2-binary>=2.9.9
duckdb>=0.9.0
python-dotenv>=1.0.0
apache-airflow>=2.7.0
pandas>=2.1.0
```

### dbt (`dbt/requirements.txt`)

```
dbt-core>=1.7.0
dbt-duckdb>=1.7.0
dbt-postgres>=1.7.0
```
