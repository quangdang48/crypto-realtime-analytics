## 1. Extraction Script

- [ ] 1.1 Create `scripts/extract_crypto.py` with `fetch_crypto_data()` function that calls CoinGecko API (`/api/v3/coins/markets?vs_currency=usd&ids=bitcoin,ethereum,solana`) with a 30-second timeout
- [ ] 1.2 Add `insert_into_postgres(records)` function that maps API fields to `staging_crypto` columns and inserts rows with transaction rollback on error
- [ ] 1.3 Add `extract_and_load()` entry point that calls fetch then insert, with logging
- [ ] 1.4 Add `if __name__ == "__main__"` block to allow standalone execution

## 2. Verification

- [ ] 2.1 Ensure PostgreSQL container is running (`docker-compose up -d`)
- [ ] 2.2 Run `python scripts/extract_crypto.py` and confirm 3 rows appear in `staging_crypto`
- [ ] 2.3 Run the script a second time and verify 3 more rows are appended (6 total)
- [ ] 2.4 Query `SELECT coin_id, price_usd, fetched_at FROM staging_crypto ORDER BY fetched_at DESC LIMIT 6;` to confirm data correctness
