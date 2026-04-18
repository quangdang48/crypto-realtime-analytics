# Change: Set up infrastructure and database

## Why

The project currently has no runnable infrastructure. We need a Docker Compose setup to run PostgreSQL (staging database) and the foundational configuration files (`.env`, `.gitignore`, SQL init script) so the pipeline has a working data layer to build on.

## What Changes

- Add `docker-compose.yml` with PostgreSQL service (using `.env` variables)
- Add `sql/init.sql` to create the `staging_crypto` table and indexes on first startup
- Add `.env.example` as a safe-to-commit template
- Add `.gitignore` to exclude secrets, caches, and generated files
- Add `requirements.txt` with core Python dependencies

## Impact

- Affected specs: `infrastructure`, `database` (new capabilities)
- Affected code: `docker-compose.yml`, `sql/init.sql`, `.env.example`, `.gitignore`, `requirements.txt`
- No breaking changes (greenfield setup)
