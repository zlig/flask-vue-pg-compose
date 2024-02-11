# flask-vue-pg-compose

Build a Python Flask web application combined with Vue.js and a PostgreSQL database in a Docker Compose file for local development

## Usage

### Prerequisites

On recent versions of Docker, Docker Compose is included, which can create a conflict with the following commands based on `docker-compose`.

A simple workaround to allow running the commands documented below is to add an alias to the .bashrc or .zshrc configuration of the current workstation or server:

```bash
alias docker-compose='docker compose'
```

An alternative and more complex solution is to create a script that respect the legacy container naming convention (allowing a `_`):

```bash
sudo cat <<EOF >> /usr/bin/docker-compose
#!/bin/bash
docker compose --compatibility "$@"
EOF

sudo chmod +x /usr/bin/docker-compose
```

Additionally, on a Linux workstation, executes the following commands to add the current user to the docker group to allow running it without `sudo`:

```bash
# Creates docker group (it should already exist)
sudo groupadd docker

# Add current user to docker group
sudo usermod -aG docker $USER

# Set ACL for user on docker socket
sudo setfacl -m user:$USER:rw /var/run/docker.sock
```

### General Usage

#### Edit configuration

Ensure to edit *.gitignore* to add `.env` if using sensitive credentials

`vim .env`

#### Build images

`docker-compose build` or `docker-compose build --progress plain --no-cache`

#### Run containers

The containers can be run as background tasks with the following command:

`docker-compose up -d`

To start the containers only in the current terminal and see the logs live, run this command instead:

`docker-compose up --remove-orphans`

#### Check logs

`docker-compose logs` or `docker-compose logs -f`

#### Check current resources usage

`docker-compose top`

#### Stop containers

`docker-compose down`

#### Containers usage

In general, the prompt for a terminal session can be opened on a pod with the following command:

`docker-compose exec <db|redis|frontend> bash`

### PostgreSQL usage

* Connect into PostgreSQL container:

`$ docker-compose exec db bash`

* Elevate to `postgres` user and launch `psql` utility:

`bash-5.1# su postgres -c psql`

* Executes commands in the PostgreSQL container:

```bash
-- Show connection info
\conninfo

-- List databases
\l

-- Connect to info database
\c info_db

-- List relations of the public schema
\dt

-- List relations of info_db schema
\dt info_db.*

-- List tables of all schemas
\dt

-- Shows help
\?

-- Quit PSQL
\q
```

### Check schema version

Execute the following commands to check the current database schema version of the running database:

```bash
# Export variables
SCHEMA_VERSION_TABLE="version"
SCRIPTS_DIR="/docker-entrypoint-initdb.d"

# Retrieve database schema version
psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -t -c "SELECT version FROM $SCHEMA_VERSION_TABLE"
```

## Perform a clean restart

To be perform a clean restart of the development environment, execute the following commands:

```bash
# Stop the container(s) and network(s)
docker-compose stop

# Delete all containers
docker rm -f $(docker ps -a -q)

# Delete all volumes from all containers on the local machine (DO NOT RUN IN PRODUCTION)
docker volume rm $(docker volume ls -q)

# Restart the containers
docker-compose up -d
```

## Local Development

Install prerequisites

```
# On RPM-based systems (Fedora, Red Hat, CentOS, Rocky)
sudo dnf install python3-devel
sudo dnf install libpq-devel

# On DEB-based systems (Debian, Ubuntu)
sudo apt-get install python3-dev
sudo apt-get install libpq-dev
```

Create Virtual Environment

```
python3 -m venv .venv
.venv/bin/pip3 install -r frontend/requirements.txt 
```

When creating the Python virtual environment, a prompt will appear in VS Code to select it as the interpreter for the workspace.

## Resources

* <https://github.com/mdn/developer-portal/blob/master/docker-compose.yml>
* <https://medium.com/freestoneinfotech/simplifying-docker-compose-operations-using-makefile-26d451456d63>
* <https://pythonspeed.com/articles/activate-virtualenv-dockerfile/>
* <https://runnable.com/docker/python/docker-compose-with-flask-apps>
* <https://testdriven.io/blog/dockerizing-flask-with-postgres-gunicorn-and-nginx/>
* <https://www.digitalocean.com/community/tutorials/how-to-use-templates-in-a-flask-application#>
* <https://stackoverflow.blog/2020/03/02/best-practices-for-rest-api-design/>
* <https://github.com/quay/quay>
* <https://www.digitalocean.com/community/tutorials/how-to-use-a-postgresql-database-in-a-flask-application>
* <https://www.digitalocean.com/community/tutorials/how-to-use-flask-sqlalchemy-to-interact-with-databases-in-a-flask-application>
* <https://github.com/microsoft/api-guidelines>
* <https://developer.mozilla.org/en-US/docs/Web/HTTP/Status>
