-- Dropping table
DROP TABLE IF EXISTS article;

-- Creation of article table
CREATE TABLE article (
	article_id SERIAL PRIMARY KEY,
	name VARCHAR(255) NOT NULL,
	description VARCHAR (255),
    created_at TIMESTAMPTZ DEFAULT Now(),
    last_updated TIMESTAMPTZ DEFAULT Now(),
	account_id SERIAL,
	FOREIGN KEY (account_id) REFERENCES account(account_id)
);

-- Update database schema version
UPDATE version SET version=3;