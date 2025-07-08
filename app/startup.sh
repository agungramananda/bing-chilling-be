#!/bin/bash

echo "Running migrations..."
alembic upgrade head

echo "Starting App..."
uvicorn main:app --host 0.0.0.0 --port 8000