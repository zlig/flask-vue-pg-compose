FROM postgres:14.1-alpine

COPY scripts /scripts
COPY script.sh /usr/local/bin/

RUN chmod +x /usr/local/bin/entrypoint.sh

ENTRYPOINT ["entrypoint.sh"]
