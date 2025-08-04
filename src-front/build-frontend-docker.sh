#!/usr/bin/env bash
set -e

ENV_FILE=".env"
BUILD_ENV_FILE=".env.build"

# Use provided tag or fallback to "latest"
IMAGE_TAG="${1:-latest}"

echo "[+] Using image tag: $IMAGE_TAG"

# Clean up previous build-env
rm -f "$BUILD_ENV_FILE"

echo "[+] Extracting VITE_ vars from $ENV_FILE..."

# Include all VITE_ variables
grep '^VITE_' "$ENV_FILE" > "$BUILD_ENV_FILE"

# Add VITE_BACKEND_HOST to production env (uncomment if needed)
# echo 'VITE_BACKEND_HOST=https://api-budgeter.peskov.biz' >> "$BUILD_ENV_FILE"

echo "[+] Building Docker image with tag: $IMAGE_TAG"

docker build \
  --build-arg BUILD_ENV_FILE="$BUILD_ENV_FILE" \
  -t "ypeskov/frontend-orgfin:$IMAGE_TAG" .