-- NOTE: PostgreSQL has restrictions on columns to not use
--	     https://www.postgresql.org/docs/current/sql-keywords-appendix.html

-- Dropping table
DROP TABLE IF EXISTS article;

-- Recreation of article table with title, content and thumbnail columns
CREATE TABLE IF NOT EXISTS article (
	article_id SERIAL PRIMARY KEY,
	title VARCHAR(255) NOT NULL,
	description VARCHAR (255),
	main TEXT,
	thumbnail VARCHAR (2048),
    created_at TIMESTAMPTZ DEFAULT Now(),
    last_updated TIMESTAMPTZ DEFAULT Now(),
	account_id SERIAL,
	FOREIGN KEY (account_id) REFERENCES account(account_id)
);

-- Update database schema version
UPDATE version SET version=5;