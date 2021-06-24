FROM postgres:12-alpine

ENV POSTGRES_DB=api-boilerplate
ENV POSTGRES_PASSWORD=r3allySecret

COPY setup.sql /docker-entrypoint-initdb.d/setup.sql
