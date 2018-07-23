#!/usr/bin/env sh
until nc -z postgres 5432; do
    echo "$(date) - waiting for postgres ..."
    sleep 1
done
echo "postgres ok"


python app.py