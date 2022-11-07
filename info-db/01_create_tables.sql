-- Dropping tables
DROP TABLE IF EXISTS content;
DROP TABLE IF EXISTS version;

-- Creation of version table
CREATE TABLE content (
	content_id SERIAL PRIMARY KEY,
	name VARCHAR(255) NOT NULL,
	description VARCHAR (255),
        last_update DATE
);

-- Creation of version table
CREATE TABLE IF NOT EXISTS version (
  version SMALLINT DEFAULT 0 NOT NULL
);
INSERT INTO version(version) VALUES ('1');
