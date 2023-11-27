-- NOTE:
--   This is the users accounts table, but 'user' is a reserved word in PostgreSQL..
--   It needs to be placed in double-quotes, i.e. "user", or use alternative table names (such as account, user_account, client, customer)

-- Dropping table
DROP TABLE IF EXISTS account;

-- Creation of account table
CREATE TABLE account (
	account_id SERIAL PRIMARY KEY,
	firstname VARCHAR(100) NOT NULL,
	lastname VARCHAR(100) NOT NULL,
	email VARCHAR(80) NOT NULL,
	biography TEXT,
    age SMALLINT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT Now(),
    last_updated TIMESTAMPTZ DEFAULT Now()
);

-- Update database schema version
UPDATE version SET version=2;
