-- NOTE:
--   This is the users' account table, but user is a reserved word in PostgreSQL..
--   It needs to be placed in double-quotes, or use alternative table names (such as account, user_account, client, customer)

-- Dropping table
DROP TABLE IF EXISTS account;

-- Creation of account table
CREATE TABLE account (
	user_id SERIAL PRIMARY KEY,
	firstname VARCHAR(100) NOT NULL,
	lastname VARCHAR(100) NOT NULL,
	email VARCHAR(80) NOT NULL,
	biography VARCHAR (255),
    age SMALLINT NOT NULL,
    created_at DATE,
    last_updated DATE
);

-- Update database schema version
UPDATE version SET version=2;
