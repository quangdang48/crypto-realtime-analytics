# infrastructure Specification

## Purpose
TBD - created by archiving change add-infrastructure-and-database. Update Purpose after archive.
## Requirements
### Requirement: Docker Compose Environment

The system SHALL provide a `docker-compose.yml` that defines all infrastructure services and can start the full local environment with a single `docker-compose up -d` command.

#### Scenario: Start PostgreSQL via Docker Compose

- **WHEN** the developer runs `docker-compose up -d` in the project root
- **THEN** a PostgreSQL 15 container starts on port 5432
- **AND** the database name, username, and password are read from the `.env` file

#### Scenario: PostgreSQL health check

- **WHEN** the PostgreSQL container is starting
- **THEN** Docker Compose SHALL run a `pg_isready` health check
- **AND** dependent services SHALL wait until PostgreSQL reports healthy

#### Scenario: Data persistence across restarts

- **WHEN** the developer stops and restarts the containers with `docker-compose down` followed by `docker-compose up -d`
- **THEN** all PostgreSQL data SHALL be preserved via a named Docker volume

### Requirement: Environment Configuration

The system SHALL use a `.env` file for all sensitive and environment-specific configuration, and provide a `.env.example` template that is safe to commit.

#### Scenario: Environment variables loaded by Docker Compose

- **WHEN** `docker-compose up` is executed
- **THEN** the `DB_NAME`, `DB_USERNAME`, `DB_PASSWORD`, `DB_HOST`, and `DB_PORT` variables from `.env` SHALL be used to configure the PostgreSQL container

#### Scenario: New developer onboarding

- **WHEN** a developer clones the repository
- **THEN** a `.env.example` file SHALL exist documenting all required environment variables with placeholder values
- **AND** `.env` SHALL be listed in `.gitignore` so secrets are never committed

### Requirement: Git Ignore Rules

The system SHALL include a `.gitignore` file that excludes secrets, generated files, and build artifacts from version control.

#### Scenario: Sensitive files excluded

- **WHEN** a developer runs `git status`
- **THEN** `.env`, `logs/`, `__pycache__/`, `*.duckdb`, and `dbt/target/` SHALL NOT appear as untracked files

### Requirement: Python Dependencies

The system SHALL declare core Python dependencies in a `requirements.txt` at the project root.

#### Scenario: Install dependencies

- **WHEN** a developer runs `pip install -r requirements.txt`
- **THEN** `requests`, `psycopg2-binary`, and `python-dotenv` SHALL be installed

