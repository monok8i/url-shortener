#!/bin/sh

set -e

echo "Running database migrations..."

for i in $(seq 1 10); do
    alembic upgrade head 2>/dev/null && break
    echo "Database not ready (attempt $i/10). Retrying in 3s..."
    sleep 3
done

alembic upgrade head

echo "Starting FastAPI server..."

# Start the FastAPI application with Uvicorn
exec python main.py