#!/bin/sh

set -e

echo "Running database migrations..."
alembic upgrade head

echo "Starting FastAPI server..."

# Start the FastAPI application with Uvicorn
python main.py