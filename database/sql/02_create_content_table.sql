-- Dropping table
DROP TABLE IF EXISTS content;

-- Creation of version table
CREATE TABLE content (
	content_id SERIAL PRIMARY KEY,
	name VARCHAR(255) NOT NULL,
	description VARCHAR (255),
        last_update DATE
);

-- Update database schema version
UPDATE version SET version=2;