-- =============================================
-- Crypto Real-time Analytics Pipeline
-- Database Initialization Script
-- =============================================

CREATE TABLE IF NOT EXISTS staging_crypto (
    id SERIAL PRIMARY KEY,
    coin_id VARCHAR(50) NOT NULL,
    symbol VARCHAR(10) NOT NULL,
    name VARCHAR(100),
    price_usd DECIMAL(18, 8),
    volume_24h DECIMAL(18, 2),
    market_cap DECIMAL(18, 2),
    price_change_percentage_24h DECIMAL(10, 4),
    fetched_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    raw_json JSONB
);

CREATE INDEX IF NOT EXISTS idx_staging_crypto_coin_id ON staging_crypto (coin_id);
CREATE INDEX IF NOT EXISTS idx_staging_crypto_fetched_at ON staging_crypto (fetched_at);
CREATE INDEX IF NOT EXISTS idx_staging_crypto_coin_time ON staging_crypto (coin_id, fetched_at);
