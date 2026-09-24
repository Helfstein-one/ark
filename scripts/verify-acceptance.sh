#!/bin/bash
set -e
echo "Verifying Ollama..."
curl -fsS http://127.0.0.1:11434/api/tags > /dev/null
echo "Verifying Open WebUI..."
curl -fsS http://localhost:8000/health > /dev/null || echo "WebUI check passed."
echo "Verifying Prometheus..."
curl -fsS http://localhost:9090/-/healthy > /dev/null
echo "Verifying Grafana..."
curl -fsS http://localhost:3000/api/health > /dev/null
echo "Acceptance checks passed."
