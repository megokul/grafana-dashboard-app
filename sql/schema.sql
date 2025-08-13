CREATE TABLE IF NOT EXISTS banking_data (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMPTZ NOT NULL,
    uniq_id UUID NOT NULL,
    trans_type VARCHAR(50) NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    amount_crr DECIMAL(10, 2) NOT NULL,
    account_holder_name VARCHAR(100) NOT NULL,
    card_presense VARCHAR(50) NOT NULL,
    merchant_category VARCHAR(50) NOT NULL,
    card_type VARCHAR(50) NOT NULL,
    card_id VARCHAR(20) NOT NULL,
    account_id UUID NOT NULL,
    account_blacklisted BOOLEAN NOT NULL,
    rules_triggered VARCHAR(100),
    rules_explanation VARCHAR(100),
    decision VARCHAR(100)
);

CREATE INDEX IF NOT EXISTS idx_banking_data_timestamp
    ON banking_data (timestamp DESC);

CREATE INDEX IF NOT EXISTS idx_banking_data_decision_ts
    ON banking_data (decision, timestamp DESC);

CREATE INDEX IF NOT EXISTS idx_banking_data_merchant_ts
    ON banking_data (merchant_category, timestamp DESC);

CREATE INDEX IF NOT EXISTS idx_banking_data_blacklisted_ts
    ON banking_data (account_blacklisted, timestamp DESC);
