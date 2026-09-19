#!/usr/bin/env bash
#
# Script to pull required Ollama models with a retry mechanism.
# Models: qwen2.5-coder:7b, deepseek-r1:7b, llama3.2:3b

set -euo pipefail

MODELS=("qwen2.5-coder:7b" "deepseek-r1:7b" "llama3.2:3b")
MAX_RETRIES=5
OLLAMA_API_URL=${OLLAMA_API_URL:-"http://127.0.0.1:11434"}

# Function to pull a model with exponential backoff
pull_model() {
    local model=$1
    local attempt=1
    local delay=2

    echo "Attempting to pull model: $model"

    while [ $attempt -le $MAX_RETRIES ]; do
        # Execute ollama pull (can be done inside container using podman exec or via API, here using CLI)
        if ollama pull "$model"; then
            echo "Successfully pulled $model"
            return 0
        else
            echo "Failed to pull $model (Attempt $attempt of $MAX_RETRIES)"
            if [ $attempt -lt $MAX_RETRIES ]; then
                echo "Retrying in $delay seconds..."
                sleep $delay
                delay=$((delay * 2)) # Exponential backoff
            fi
        fi
        attempt=$((attempt + 1))
    done

    echo "Error: Failed to pull model $model after $MAX_RETRIES attempts."
    return 1
}

# Ensure ollama is accessible
if ! command -v ollama &> /dev/null; then
    echo "Warning: 'ollama' CLI not found. If running inside a container, ensure this script is executed inside it."
    # Fallback to API if CLI is missing? Let's assume CLI is available or executed within pod.
fi

# Pull each model
for model in "${MODELS[@]}"; do
    pull_model "$model"
done

echo "All models processed."
