#!/bin/sh
set -e

psql -v ON_ERROR_STOP=1 \
        -v sf_db_name="$SF_DATABASE_NAME" \
        -v sf_username="$SF_DATABASE_USER" \
        -v sf_password="'$SF_DATABASE_PASSWORD'" \
        --username "$POSTGRES_USER" \
        --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE USER :sf_username WITH PASSWORD :sf_password;
    CREATE DATABASE :sf_db_name;
    GRANT ALL PRIVILEGES ON DATABASE :sf_db_name TO :sf_username;
EOSQL

psql -v ON_ERROR_STOP=1 \
        --username "$POSTGRES_USER" \
        --dbname "$SF_DATABASE_NAME" <<-EOSQL
    CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
EOSQL