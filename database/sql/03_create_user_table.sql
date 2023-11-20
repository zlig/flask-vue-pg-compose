-- NOTE:
--       user is a reserved word in PostgreSQL and needs to be placed in double-quotes
--       (or use alternative table names such as user_account, client, customer)

-- Dropping table
DROP TABLE IF EXISTS "user";

-- Creation of version table
CREATE TABLE "user" (
	user_id SERIAL PRIMARY KEY,
	name VARCHAR(255) NOT NULL,
	biography VARCHAR (255),
    last_update DATE
);

-- Update database schema version
UPDATE version SET version=3;
