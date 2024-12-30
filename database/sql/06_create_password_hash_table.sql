-- Dropping table
DROP TABLE IF EXISTS password_hash;

-- Recreation of article table with title, content and thumbnail columns
CREATE TABLE IF NOT EXISTS password_hash (
	password_hash_id SERIAL PRIMARY KEY,
	password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT Now(),
    last_updated TIMESTAMPTZ DEFAULT Now(),
	FOREIGN KEY (account_id) REFERENCES account(account_id)
);

-- Update database schema version
UPDATE version SET version=6;
