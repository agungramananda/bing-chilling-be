#!/bin/bash
set -e

if [ -z "$POSTGRES_PASSWORD" ]; then
    echo "Error: POSTGRES_PASSWORD environment variable is not set."
    exit 1
fi

echo "Replica: Waiting for master at 'master:5432' to be ready..."
until pg_isready -h master -p 5432 -U postgres; do
    sleep 1
done
echo "Replica: Master detected, continuing process..."

echo "Replica: Cleaning data directory..."
rm -rf /var/lib/postgresql/data/*

echo "Replica: Running pg_basebackup from master..."
PGPASSWORD=$POSTGRES_PASSWORD pg_basebackup \
    -h master \
    -U postgres \
    -D /var/lib/postgresql/data \
    -Fp \
    -Xs \
    -R

echo "Replica: Setting permissions and ownership of data directory..."
chmod 0700 /var/lib/postgresql/data
chown -R postgres:postgres /var/lib/postgresql/data

echo "Replica: Backup completed. Starting PostgreSQL server..."

exec gosu postgres postgres
