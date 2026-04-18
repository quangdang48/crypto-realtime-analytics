## Context

This is the first infrastructure setup for the project. Currently only documentation, `.env` (partial), and an empty `scripts/__init__.py` exist. The goal is to provide a single-command local environment that other pipeline components (extraction scripts, Airflow, dbt) will build on later.

## Goals / Non-Goals

- **Goals**: Working PostgreSQL in Docker, auto-initialized schema, proper env/config hygiene
- **Non-Goals**: Airflow services (separate change), dbt setup (separate change), extraction scripts (separate change)

## Decisions

- **PostgreSQL via Docker Compose** (not a local install): Reproducible across machines, aligns with project convention of containerized services.
- **`sql/init.sql` mounted to `/docker-entrypoint-initdb.d/`**: PostgreSQL auto-runs scripts in this directory on first container creation. Simpler than a migration tool for the initial schema.
- **`IF NOT EXISTS` everywhere**: The init script must be idempotent since it runs each time a fresh volume is created.
- **`.env` loaded via `env_file` + variable substitution**: Docker Compose reads `.env` natively. Python scripts use `python-dotenv`. Single source of truth for credentials.
- **No Airflow services yet**: Infrastructure is scoped to PostgreSQL only. Airflow will be a separate change to keep proposals small and reviewable.

## Risks / Trade-offs

- **Single PostgreSQL for both staging and Airflow metadata** (future): When Airflow is added later, it will share this same PostgreSQL instance. Acceptable for a local learning project; in production you'd separate them.
- **No migration tool**: Using raw `init.sql` is simple but doesn't support incremental schema changes. If schema evolves significantly, a migration tool (e.g., Alembic) should be introduced.

## Open Questions

- None — scope is straightforward for a local dev setup.
