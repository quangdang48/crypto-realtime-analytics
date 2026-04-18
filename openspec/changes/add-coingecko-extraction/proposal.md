# Change: Add CoinGecko extraction script

## Why

The pipeline has a running PostgreSQL database with the `staging_crypto` table, but no way to populate it. We need a Python script that fetches live cryptocurrency data from the CoinGecko API and inserts it into the staging table — completing the **Extract** stage of the pipeline.

## What Changes

- Create `scripts/extract_crypto.py` with functions to fetch data from CoinGecko and insert into PostgreSQL
- Update `requirements.txt` if any new dependencies are needed (none expected — `requests`, `psycopg2-binary`, `python-dotenv` already declared)

## Impact

- Affected specs: `extraction` (new capability)
- Affected code: `scripts/extract_crypto.py`
- Depends on: `database` spec (staging_crypto table must exist), `infrastructure` spec (.env config)
- No breaking changes
