## 1. Extraction Script

PS C:\Learn\crypto-realtime-analytics-pipeline> py .\scripts\extract_crypto.py
Traceback (most recent call last):
  File "C:\Learn\crypto-realtime-analytics-pipeline\scripts\extract_crypto.py", line 6, in <module>
    import psycopg2
ModuleNotFoundError: No module named 'psycopg2'
PS C:\Learn\crypto-realtime-analytics-pipeline> - [x] 1.1 Create `scripts/extract_crypto.py` with `fetch_crypto_data()` function that calls CoinGecko API (`/api/v3/coins/markets?vs_currency=usd&ids=bitcoin,ethereum,solana`) with a 30-second timeout
- [x] 1.2 Add `insert_into_postgres(records)` function that maps API fields to `staging_crypto` columns and inserts rows with transaction rollback on error
- [x] 1.3 Add `extract_and_load()` entry point that calls fetch then insert, with logging
- [x] 1.4 Add `if __name__ == "__main__"` block to allow standalone execution

## 2. Verification

- [ ] 2.1 Ensure PostgreSQL container is running (`docker-compose up -d`)
- [ ] 2.2 Run `python scripts/extract_crypto.py` and confirm 3 rows appear in `staging_crypto`
- [ ] 2.3 Run the script a second time and verify 3 more rows are appended (6 total)
- [ ] 2.4 Query `SELECT coin_id, price_usd, fetched_at FROM staging_crypto ORDER BY fetched_at DESC LIMIT 6;` to confirm data correctness
