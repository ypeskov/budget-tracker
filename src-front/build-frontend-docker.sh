#!/usr/bin/env bash
set -e

ENV_FILE=".env"
BUILD_ENV_FILE=".env.build"

# Clean up previous build-env
rm -f $BUILD_ENV_FILE

echo "[+] Extracting VITE_ vars from $ENV_FILE..."

# Filter all except VITE_BACKEND_HOST
grep '^VITE_' "$ENV_FILE" | grep -v '^VITE_BACKEND_HOST=' > $BUILD_ENV_FILE

# Add VITE_BACKEND_HOST to production env
echo 'VITE_BACKEND_HOST=https://api-budgeter.peskov.biz' >> $BUILD_ENV_FILE

echo "[+] Building Docker image..."

docker build \
  --build-arg BUILD_ENV_FILE=$BUILD_ENV_FILE \
  -t ypeskov/frontend-orgfin .