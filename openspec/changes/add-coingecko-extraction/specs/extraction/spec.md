## ADDED Requirements

### Requirement: CoinGecko API Data Fetching

The system SHALL fetch current market data for BTC, ETH, and SOL from the CoinGecko `/api/v3/coins/markets` endpoint.

#### Scenario: Successful API fetch

- **WHEN** the extraction script calls the CoinGecko API with `vs_currency=usd` and `ids=bitcoin,ethereum,solana`
- **THEN** it SHALL return parsed market data for each coin including `current_price`, `total_volume`, `market_cap`, and `price_change_percentage_24h`

#### Scenario: API request timeout

- **WHEN** the CoinGecko API does not respond within 30 seconds
- **THEN** the script SHALL raise a timeout error rather than hanging indefinitely

#### Scenario: API error response

- **WHEN** the CoinGecko API returns an HTTP error status (4xx or 5xx)
- **THEN** the script SHALL raise an exception with the status code for upstream handling

### Requirement: Data Insertion into Staging Table

The system SHALL insert fetched coin data into the `staging_crypto` PostgreSQL table, mapping API response fields to table columns.

#### Scenario: Successful insertion

- **WHEN** the API returns data for 3 coins
- **THEN** 3 rows SHALL be inserted into `staging_crypto` with `coin_id`, `symbol`, `name`, `price_usd`, `volume_24h`, `market_cap`, `price_change_percentage_24h`, `fetched_at` (UTC), and `raw_json` (full API response per coin)

#### Scenario: Database connection uses environment variables

- **WHEN** the script connects to PostgreSQL
- **THEN** it SHALL read `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USERNAME`, and `DB_PASSWORD` from environment variables (loaded via `python-dotenv`)

#### Scenario: Transaction safety

- **WHEN** an error occurs during insertion of any row
- **THEN** the transaction SHALL be rolled back so no partial data is committed
- **AND** the database connection SHALL be closed

### Requirement: Callable Entry Point

The system SHALL expose an `extract_and_load()` function that performs the full fetch-and-insert cycle, suitable for direct invocation and future Airflow integration.

#### Scenario: Run as standalone script

- **WHEN** a developer runs `python scripts/extract_crypto.py`
- **THEN** it SHALL execute `extract_and_load()` and log the number of records inserted

#### Scenario: Import as module

- **WHEN** another module imports `extract_and_load` from `scripts.extract_crypto`
- **THEN** it SHALL be callable without side effects from the import itself
