#!/bin/sh

while ! nc -z db 5432; do
  sleep 0.1
done

echo "Postgres did run"

uvicorn main:app --reload --host 0.0.0.0 --port 8000

echo "Pastebin API has started"

exec "$@"
