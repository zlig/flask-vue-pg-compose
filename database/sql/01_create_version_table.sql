-- Dropping table
DROP TABLE IF EXISTS version;

-- Creation of version table
CREATE TABLE IF NOT EXISTS version (
  version SMALLINT DEFAULT 0 NOT NULL
);
INSERT INTO version(version) VALUES ('1');
