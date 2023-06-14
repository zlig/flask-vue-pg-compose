#!/usr/bin/env bash
#
# Applies schema updates to database
#
set -x
set -e

whoami

# Create a directory to store the schema versions
mkdir -p /var/lib/postgresql/schema

# Get the current schema version
if [ -f /var/lib/postgresql/schema/version.txt ]; then
  CURRENT_VERSION=$(cat /var/lib/postgresql/schema/version.txt)
else
  CURRENT_VERSION=0
fi

# Loop through the SQL scripts and apply them if they are newer than the current version
for SCRIPT in $(ls /scripts/*.sql); do
  SCRIPT_NAME=$(basename $SCRIPT .sql)
  SCRIPT_VERSION=$(echo $SCRIPT_NAME | cut -d'_' -f1)

  if [ $SCRIPT_VERSION -gt $CURRENT_VERSION ]; then
    echo "Applying $SCRIPT_NAME"
    psql -U postgres -d mydb -f $SCRIPT
    echo $SCRIPT_VERSION > /var/lib/postgresql/schema/version.txt
  fi
done

# Executes all schema updates above current version
echo "Database exists, updating database schema..."
for SQL_FILE in \`ls /scripts/schema_update_*.sql\`;
do
  UPDATE_VERSION=\`echo \$SQL_FILE | sed "s|/scripts/schema_update_||" | sed "s|.sql||"\`

  if [[ "\$UPDATE_VERSION" -gt "\$DBVERSION" ]]; then
    echo "Applying schema updates from file \$SQL_FILE to update database schema to version \$UPDATE_VERSION"
    psql -U postgres -d mydb -f $SCRIPT
  fi
done

set -x

# Start the PostGreSQL server
exec /usr/local/bin/docker-entrypoint.sh "$@"

