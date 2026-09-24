#!/usr/bin/env bash
set -e

CERTS_DIR="$(dirname "$0")/../certs"
mkdir -p "$CERTS_DIR"

if [ ! -f "$CERTS_DIR/cert.crt" ] || [ ! -f "$CERTS_DIR/cert.key" ]; then
    echo "Generating self-signed SSL/TLS certificates..."
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
        -keyout "$CERTS_DIR/cert.key" \
        -out "$CERTS_DIR/cert.crt" \
        -subj "/C=US/ST=State/L=City/O=ProjectARK/OU=Dev/CN=localhost"
    echo "Certificates generated in $CERTS_DIR"
else
    echo "Certificates already exist in $CERTS_DIR, skipping generation."
fi
