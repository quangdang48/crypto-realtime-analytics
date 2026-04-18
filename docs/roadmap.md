# Implementation Roadmap

A 4-week plan to build the Crypto Real-time Analytics Pipeline from scratch.

---

## Week 1: Foundation — Docker + PostgreSQL + Python Extraction

### Goals

- Set up the development environment
- Write a working Python script to fetch crypto data from an API
- Insert raw data into PostgreSQL

### Tasks

- [ ] **1.1** Install Docker Desktop and verify it's running

  ```bash
  docker --version
  docker-compose --version
  ```

- [ ] **1.2** Create `docker-compose.yml` with PostgreSQL service

  ```yaml
  services:
    postgres:
      image: postgres:15-alpine
      environment:
        POSTGRES_DB: crypto_db
        POSTGRES_USER: crypto_user
        POSTGRES_PASSWORD: crypto_pass
      ports:
        - '5432:5432'
      volumes:
        - postgres_data:/var/lib/postgresql/data
  ```

- [ ] **1.3** Create the `staging_crypto` table in PostgreSQL

  ```sql
  CREATE TABLE staging_crypto (
      id SERIAL PRIMARY KEY,
      coin_id VARCHAR(50) NOT NULL,
      symbol VARCHAR(10) NOT NULL,
      name VARCHAR(100),
      price_usd DECIMAL(18, 8),
      volume_24h DECIMAL(18, 2),
      market_cap DECIMAL(18, 2),
      price_change_percentage_24h DECIMAL(10, 4),
      fetched_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
      raw_json JSONB
  );
  ```

- [ ] **1.4** Write `scripts/extract_crypto.py` — Python script using `requests`
  - Call CoinGecko API: `GET /api/v3/coins/markets?vs_currency=usd&ids=bitcoin,ethereum,solana`
  - Parse JSON response
  - Insert each coin's data into `staging_crypto` using `psycopg2`

- [ ] **1.5** Run the script manually and verify data appears in PostgreSQL

### Deliverables

- Docker Compose running PostgreSQL
- Python script that fetches and stores crypto data
- At least 10 rows of data in `staging_crypto`

### Learning Resources

- [CoinGecko API Docs](https://www.coingecko.com/en/api/documentation)
- [psycopg2 Tutorial](https://www.psycopg.org/docs/usage.html)
- [Docker Compose Getting Started](https://docs.docker.com/compose/gettingstarted/)

---

## Week 2: Orchestration — Apache Airflow Setup

### Goals

- Set up Airflow using Docker Compose
- Write a basic DAG with a "Hello World" task
- Understand Airflow concepts (DAG, Task, Operator, Schedule)

### Tasks

- [ ] **2.1** Add Airflow services to `docker-compose.yml`
  - `airflow-webserver` (UI on port 8080)
  - `airflow-scheduler` (executes tasks)
  - `airflow-init` (one-time DB setup)
  - Shared volumes for DAGs folder

- [ ] **2.2** Start Airflow and log in to the web UI
  - Default credentials: `airflow` / `airflow`
  - Navigate to http://localhost:8080

- [ ] **2.3** Write a "Hello World" DAG in `dags/hello_world.py`

  ```python
  from airflow import DAG
  from airflow.operators.python import PythonOperator
  from datetime import datetime

  def say_hello():
      print("Hello from Airflow!")

  with DAG(
      dag_id="hello_world",
      start_date=datetime(2024, 1, 1),
      schedule_interval="@daily",
      catchup=False,
  ) as dag:
      task = PythonOperator(
          task_id="hello_task",
          python_callable=say_hello,
      )
  ```

- [ ] **2.4** Trigger the DAG manually from the Airflow UI and check logs

- [ ] **2.5** Experiment with different schedule intervals
  - `@hourly`, `@daily`, `*/5 * * * *` (every 5 minutes)

### Deliverables

- Airflow running in Docker alongside PostgreSQL
- A working "Hello World" DAG visible in the Airflow UI
- Understanding of DAG, Task, Operator, and Schedule concepts

### Learning Resources

- [Airflow Tutorial](https://airflow.apache.org/docs/apache-airflow/stable/tutorial/index.html)
- [Airflow Docker Compose](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html)

---

## Week 3: Integration — Automated Data Pipeline

### Goals

- Connect the Python extraction script (Week 1) to Airflow (Week 2)
- Have a fully automated Extract & Load system running every 5 minutes

### Tasks

- [ ] **3.1** Move the extraction logic into a callable Python function

  ```python
  # scripts/extract_crypto.py
  def extract_and_load():
      """Fetch crypto data from API and insert into PostgreSQL."""
      # ... extraction logic here
  ```

- [ ] **3.2** Create `dags/crypto_pipeline.py` DAG

  ```python
  from airflow import DAG
  from airflow.operators.python import PythonOperator
  from datetime import datetime
  import sys
  sys.path.insert(0, "/opt/airflow/scripts")
  from extract_crypto import extract_and_load

  with DAG(
      dag_id="crypto_pipeline",
      start_date=datetime(2024, 1, 1),
      schedule_interval="*/5 * * * *",
      catchup=False,
  ) as dag:
      extract_task = PythonOperator(
          task_id="extract_crypto_data",
          python_callable=extract_and_load,
      )
  ```

- [ ] **3.3** Mount the `scripts/` directory into the Airflow container

- [ ] **3.4** Enable the DAG in the Airflow UI and let it run for a few hours

- [ ] **3.5** Verify data is accumulating in PostgreSQL

  ```sql
  SELECT coin_id, COUNT(*), MIN(fetched_at), MAX(fetched_at)
  FROM staging_crypto
  GROUP BY coin_id;
  ```

- [ ] **3.6** Add error handling and logging to the extraction script

### Deliverables

- Airflow DAG running every 5 minutes automatically
- Data continuously accumulating in PostgreSQL
- Ability to monitor pipeline health in Airflow UI

---

## Week 4: Transform & Visualize — dbt + Dashboard

### Goals

- Set up dbt to transform raw data into analytical models
- Create a simple dashboard to visualize crypto trends

### Tasks

- [ ] **4.1** Install dbt with DuckDB adapter

  ```bash
  pip install dbt-core dbt-duckdb
  dbt init crypto_analytics
  ```

- [ ] **4.2** Configure `profiles.yml` for DuckDB connection

- [ ] **4.3** Create staging model: `models/staging/stg_crypto_prices.sql`

  ```sql
  SELECT
      id,
      coin_id,
      symbol,
      price_usd,
      volume_24h,
      market_cap,
      price_change_percentage_24h,
      fetched_at,
      DATE(fetched_at) AS price_date,
      EXTRACT(HOUR FROM fetched_at) AS price_hour
  FROM {{ source('crypto', 'staging_crypto') }}
  ```

- [ ] **4.4** Create mart models:
  - `fct_price_hourly.sql` — Hourly aggregated prices
  - `fct_moving_average.sql` — 1-hour rolling average
  - `fct_volatility.sql` — Price spread (high - low)

- [ ] **4.5** Add dbt tests for data quality

  ```yaml
  # models/staging/schema.yml
  models:
    - name: stg_crypto_prices
      columns:
        - name: coin_id
          tests:
            - not_null
            - accepted_values:
                values: ['bitcoin', 'ethereum', 'solana']
        - name: price_usd
          tests:
            - not_null
  ```

- [ ] **4.6** Run dbt and verify models

  ```bash
  dbt run
  dbt test
  dbt docs generate
  dbt docs serve
  ```

- [ ] **4.7** Set up Evidence.dev or Metabase for visualization
  - Connect to DuckDB warehouse
  - Create price trend line chart
  - Create volume comparison chart

### Deliverables

- dbt models transforming raw data into analytical tables
- Moving average, volatility, and hourly aggregation models
- A dashboard with at least 2-3 charts showing crypto trends

---

## Beyond Week 4: Stretch Goals

| Goal                 | Description                                                      |
| -------------------- | ---------------------------------------------------------------- |
| Add more coins       | Extend to top 20 coins by market cap                             |
| Alerting             | Send Slack/email alerts when volatility exceeds threshold        |
| Data quality         | Add Great Expectations or dbt tests for comprehensive validation |
| CI/CD                | GitHub Actions to run dbt tests on every PR                      |
| Cloud deployment     | Deploy to a cloud VM (AWS EC2 free tier / GCP)                   |
| Capstone integration | Apply ETL patterns to log processing or revenue analytics        |

---

## Tips for Capstone Project

> If you incorporate ETL thinking into your Capstone project (e.g., processing application logs or computing revenue statistics), it will significantly boost both your grade and your resume for Backend/Data Engineering roles.

Possible Capstone integrations:

- **Log analytics**: Collect application logs → ETL into warehouse → Dashboard for error rates, response times
- **Revenue reporting**: Extract transaction data → Transform into daily/monthly aggregates → Executive dashboard
