# flask-vue-pg-compose

Build a Python Flask web application combined with Vue.js and a PostgreSQL database in a Docker Compose file for local development

## Usage

### Edit configuration

Ensure to edit *.gitignore* to add `.env` if using sensitive credentials

`vim .env`


### Build images

`docker-compose build` or `docker-compose build --progress plain --no-cache`

### Run containers

`docker-compose up -d`

### Check logs

`docker-compose logs` or `docker-compose logs -f`

### Check current resources usage

`docker-compose top`

### Stop containers

`docker-compose down`

### Extras

Use `docker scan` to run Snyk tests against images to find vulnerabilities and learn how to fix them

## Resources

- https://github.com/mdn/developer-portal/blob/master/docker-compose.yml
- https://medium.com/freestoneinfotech/simplifying-docker-compose-operations-using-makefile-26d451456d63
- https://pythonspeed.com/articles/activate-virtualenv-dockerfile/
- https://runnable.com/docker/python/docker-compose-with-flask-apps
- https://testdriven.io/blog/dockerizing-flask-with-postgres-gunicorn-and-nginx/
- https://www.digitalocean.com/community/tutorials/how-to-use-templates-in-a-flask-application#
- https://stackoverflow.blog/2020/03/02/best-practices-for-rest-api-design/
