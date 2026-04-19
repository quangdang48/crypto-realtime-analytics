import json
import logging
import os
from datetime import datetime, timezone

import psycopg2
import requests
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

COINGECKO_API_URL = "https://api.coingecko.com/api/v3/coins/markets"
TARGET_COINS = "bitcoin,ethereum,solana"
VS_CURRENCY = "usd"

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", "5432"),
    "dbname": os.getenv("DB_NAME", "crypto_analytics_realtime"),
    "user": os.getenv("DB_USERNAME", "postgres"),
    "password": os.getenv("DB_PASSWORD", "password"),
}


def fetch_crypto_data():
    params = {
        "vs_currency": VS_CURRENCY,
        "ids": TARGET_COINS,
        "order": "market_cap_desc",
        "per_page": 10,
        "page": 1,
        "sparkline": "false",
        "price_change_percentage": "24h",
    }

    logger.info("Fetching crypto data from CoinGecko API...")
    response = requests.get(COINGECKO_API_URL, params=params, timeout=30)
    response.raise_for_status()

    data = response.json()
    logger.info("Fetched data for %d coins", len(data))
    return data


def insert_into_postgres(records):
    insert_query = """
        INSERT INTO staging_crypto (
            coin_id, symbol, name, price_usd, volume_24h,
            market_cap, price_change_percentage_24h, fetched_at, raw_json
        ) VALUES (
            %(coin_id)s, %(symbol)s, %(name)s, %(price_usd)s, %(volume_24h)s,
            %(market_cap)s, %(price_change_percentage_24h)s, %(fetched_at)s, %(raw_json)s
        )
    """

    conn = None
    inserted = 0
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        now = datetime.now(timezone.utc)

        for record in records:
            row = {
                "coin_id": record.get("id"),
                "symbol": record.get("symbol"),
                "name": record.get("name"),
                "price_usd": record.get("current_price"),
                "volume_24h": record.get("total_volume"),
                "market_cap": record.get("market_cap"),
                "price_change_percentage_24h": record.get("price_change_percentage_24h"),
                "fetched_at": now,
                "raw_json": json.dumps(record),
            }
            cursor.execute(insert_query, row)
            inserted += 1

        conn.commit()
        logger.info("Inserted %d records into staging_crypto", inserted)
    except psycopg2.Error as e:
        logger.error("Database error: %s", e)
        if conn:
            conn.rollback()
        raise
    finally:
        if conn:
            conn.close()

    return inserted


def extract_and_load():
    logger.info("Starting extraction pipeline at %s", datetime.now(timezone.utc))

    records = fetch_crypto_data()
    if not records:
        logger.warning("No records fetched from API")
        return 0

    count = insert_into_postgres(records)
    logger.info("Pipeline completed. %d records inserted.", count)
    return count


if __name__ == "__main__":
    extract_and_load()
