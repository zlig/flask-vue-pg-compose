-- Dropping table
DROP TABLE IF EXISTS article;

-- Creation of article table
CREATE TABLE article (
	article_id SERIAL PRIMARY KEY,
	name VARCHAR(255) NOT NULL,
	description VARCHAR (255),
    last_update DATE,
	account_id SERIAL,
	FOREIGN KEY (account_id) REFERENCES account(account_id)
);

-- Update database schema version
UPDATE version SET version=3;