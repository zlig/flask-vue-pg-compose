-- Dropping table
DROP TABLE IF EXISTS api_token;

-- Recreation of article table with title, content and thumbnail columns
CREATE TABLE IF NOT EXISTS api_token (
	api_token_id SERIAL PRIMARY KEY,
	api_token VARCHAR(255) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT Now(),
    last_updated TIMESTAMPTZ DEFAULT Now(),
	account_id SERIAL,
	FOREIGN KEY (account_id) REFERENCES account(account_id)
);

-- Update database schema version
UPDATE version SET version=7;
