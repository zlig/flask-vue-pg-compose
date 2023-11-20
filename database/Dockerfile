FROM postgres:14.1-alpine


COPY sql/*.sql /docker-entrypoint-initdb.d/
COPY entrypoint.sh /usr/local/bin/

RUN chmod +x /usr/local/bin/entrypoint.sh

ENTRYPOINT ["entrypoint.sh"]

CMD ["postgres"]
