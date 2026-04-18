## ADDED Requirements

### Requirement: Staging Table Schema

The system SHALL create a `staging_crypto` table in PostgreSQL to store raw cryptocurrency market data fetched from external APIs.

#### Scenario: Table created on first startup

- **WHEN** the PostgreSQL container starts for the first time
- **THEN** the `staging_crypto` table SHALL be created automatically via `sql/init.sql` mounted to `/docker-entrypoint-initdb.d/`
- **AND** the table SHALL have the following columns: `id` (SERIAL PK), `coin_id` (VARCHAR), `symbol` (VARCHAR), `name` (VARCHAR), `price_usd` (DECIMAL), `volume_24h` (DECIMAL), `market_cap` (DECIMAL), `price_change_percentage_24h` (DECIMAL), `fetched_at` (TIMESTAMP WITH TIME ZONE), `raw_json` (JSONB)

#### Scenario: Idempotent table creation

- **WHEN** the init script runs on a database where the table already exists
- **THEN** the script SHALL use `CREATE TABLE IF NOT EXISTS` and complete without error

### Requirement: Database Indexes

The system SHALL create indexes on the `staging_crypto` table to support efficient queries by coin and time range.

#### Scenario: Indexes created on first startup

- **WHEN** the `staging_crypto` table is created
- **THEN** indexes SHALL exist on `coin_id`, `fetched_at`, and the composite `(coin_id, fetched_at)`
- **AND** all indexes SHALL use `CREATE INDEX IF NOT EXISTS` for idempotency

### Requirement: Raw Data Preservation

The system SHALL store the complete API response alongside parsed fields to allow future reprocessing without re-fetching.

#### Scenario: Full API response stored

- **WHEN** a row is inserted into `staging_crypto`
- **THEN** the `raw_json` column SHALL contain the full JSON response for that coin as a JSONB value

### Requirement: Timezone-Aware Timestamps

The system SHALL store all timestamps with timezone information to support correct cross-timezone analytics.

#### Scenario: Fetch timestamp recorded

- **WHEN** a row is inserted into `staging_crypto`
- **THEN** the `fetched_at` column SHALL default to `NOW()` and store a `TIMESTAMP WITH TIME ZONE` value
