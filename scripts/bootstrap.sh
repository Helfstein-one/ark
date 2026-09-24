#!/usr/bin/env bash

echo "Starting Project A.R.K. containers..."
docker compose up -d

echo "Waiting for containers to initialize (15 seconds)..."
sleep 15

echo "Pulling default LLMs..."
docker compose exec ollama /scripts/pull-models.sh

echo "Bootstrap complete. Services are ready."
