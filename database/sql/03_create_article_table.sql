-- Dropping table
DROP TABLE IF EXISTS article;

-- Creation of article table
CREATE TABLE article (
	article_id SERIAL PRIMARY KEY,
	name VARCHAR(255) NOT NULL,
	description VARCHAR (255),
    last_update DATE
);

-- Update database schema version
UPDATE version SET version=3;