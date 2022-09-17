#!/bin/bash
set -e

docker compose up --build --force-recreate --no-deps -d frontend
docker compose cp frontend:/app/build/. ./frontend/build

docker compose down
