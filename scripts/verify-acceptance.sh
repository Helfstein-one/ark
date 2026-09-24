#!/bin/bash
set -e
echo "Verifying Open WebUI via Reverse Proxy (HTTPS)..."
curl -k -fsS https://localhost/ > /dev/null || curl -k -fsS https://127.0.0.1/ > /dev/null
echo "Verifying Ollama is not publicly exposed on host..."
if curl -s --connect-timeout 2 http://127.0.0.1:11434/api/tags > /dev/null; then
    echo "ERROR: Ollama port 11434 is exposed to host!"
    exit 1
else
    echo "Ollama port 11434 is properly restricted from host."
fi
echo "Acceptance checks passed."
