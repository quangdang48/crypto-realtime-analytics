## 1. Project Configuration Files

- [x] 1.1 Add `DB_HOST` and `DB_PORT` to `.env` (currently only has `DB_NAME`, `DB_USERNAME`, `DB_PASSWORD`)
- [x] 1.2 Create `.env.example` with all required variables and placeholder values
- [x] 1.3 Create `.gitignore` excluding `.env`, `logs/`, `__pycache__/`, `*.duckdb`, `dbt/target/`, `dbt/dbt_packages/`
- [x] 1.4 Create `requirements.txt` with `requests`, `psycopg2-binary`, `python-dotenv`

## 2. Database Schema

- [x] 2.1 Create `sql/init.sql` with `CREATE TABLE IF NOT EXISTS staging_crypto` and all columns per spec
- [x] 2.2 Add `CREATE INDEX IF NOT EXISTS` statements for `coin_id`, `fetched_at`, and composite `(coin_id, fetched_at)`

## 3. Docker Compose

- [x] 3.1 Create `docker-compose.yml` with PostgreSQL service using `postgres:15-alpine`
- [x] 3.2 Configure service to read `DB_NAME`, `DB_USERNAME`, `DB_PASSWORD` from `.env` via `env_file` and variable substitution
- [x] 3.3 Mount `sql/init.sql` to `/docker-entrypoint-initdb.d/` for auto-initialization
- [x] 3.4 Add `pg_isready` health check on the PostgreSQL service
- [x] 3.5 Add named volume `postgres_data` for data persistence
- [x] 3.6 Define `crypto_network` bridge network

## 4. Verification

- [ ] 4.1 Run `docker-compose up -d` and confirm PostgreSQL starts healthy
- [ ] 4.2 Connect to the database and verify `staging_crypto` table and indexes exist
- [ ] 4.3 Run `docker-compose down` then `docker-compose up -d` and verify data persists
