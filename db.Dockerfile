FROM postgres:17.6-bookworm

COPY sql/*.sql /docker-entrypoint-initdb.d/

EXPOSE 5432
