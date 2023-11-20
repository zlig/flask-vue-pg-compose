#!/usr/bin/env bash
#
# Applies schema updates to database
#
set -x
set -e

# Define variables
SCHEMA_VERSION_TABLE="version"
SCRIPTS_DIR="/docker-entrypoint-initdb.d"

# # DEBUG
# echo "Displaying debug information.."
# whoami
# pwd
# ls -l $SCRIPTS_DIR


# Versions the database schema (if it exists)
echo
echo "Versioning database schema.."

# look specifically for PG_VERSION, as it is expected in the DB dir
declare -g DATABASE_ALREADY_EXISTS
if [ -s "$PGDATA/PG_VERSION" ]; then
  DATABASE_ALREADY_EXISTS='true'
fi

# Applies update script if database already exists
if [ ! -z "$DATABASE_ALREADY_EXISTS" ]; then

  # Reuse PostgreSQL script as library of functions
  source /usr/local/bin/docker-entrypoint.sh
  docker_setup_env
  set +x

  # Temporarily start PostgreSQL server
  su -l $POSTGRES_USER -c "pg_ctl start -s -l /dev/null -D $PGDATA"

  # Get current schema version
  CURRENT_VERSION=$(psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -t -c "SELECT version FROM $SCHEMA_VERSION_TABLE" | xargs)

  # Apply SQL scripts
  for script in $(ls $SCRIPTS_DIR/*.sql | sort -V); do

    # Get script version
    SCRIPT_VERSION=$(echo $script | sed -E 's/.*\/([0-9]+)[\_\-].*/\1/')

    # Applying SQL script (if applicable)
    echo "Checking if script version $SCRIPT_VERSION should be applied on current database schema version $CURRENT_VERSION"
    if [ $SCRIPT_VERSION -gt $CURRENT_VERSION ]; then
      echo "Applying script $script"
      docker_process_init_files $script
    fi
  done

  # Stop temporary instance of PostgreSQL server
  su -l $POSTGRES_USER -c "pg_ctl stop -s -l /dev/null -D $PGDATA"
  unset DATABASE_ALREADY_EXISTS
  set -x

  # Process completed
  echo
  echo 'PostgreSQL schema update process completed; ready for start up.'

else

  # New database
  echo
  echo 'PostgreSQL schema update not required on a new database.'

fi


# Start the PostGreSQL server
echo
echo "Starting postgres.."
exec /usr/local/bin/docker-entrypoint.sh "$@"
