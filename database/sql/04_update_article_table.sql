-- NOTE: PostgreSQL does support adding a column at a specific location

-- Dropping table
DROP TABLE IF EXISTS article;

-- Recreation of article table with new title column
CREATE TABLE IF NOT EXISTS article (
	article_id SERIAL PRIMARY KEY,
	title VARCHAR(255) NOT NULL,
	name VARCHAR(255) NOT NULL,
	description VARCHAR (255),
    created_at TIMESTAMPTZ DEFAULT Now(),
    last_updated TIMESTAMPTZ DEFAULT Now(),
	account_id SERIAL,
	FOREIGN KEY (account_id) REFERENCES account(account_id)
);

-- Update database schema version
UPDATE version SET version=4;