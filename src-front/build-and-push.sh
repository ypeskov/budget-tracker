#!/usr/bin/env bash
set -euo pipefail

IMAGE_NAME="ypeskov/frontend-orgfin"
TAG=""
ENV="prod"
ENV_FILE=""
BUILD_ENV_FILE=".env.build"
PLATFORM_ARG="--platform=linux/arm64"
PUSH=false

# Display help message
show_help() {
    cat << EOF
Usage: $(basename "$0") TAG [OPTIONS]

Build and optionally push Docker image for OrgFin Frontend.

TAG:
    Required. The tag name for the Docker image (e.g., 1.2.3)

OPTIONS:
    --help                  Show this help message and exit
    --push                  Push the built image to Docker registry
    --platform=PLATFORM     Set target platform for the build
                           (default: linux/arm64)
    --env=ENV              Environment to use (default: prod)

EXAMPLES:
    $(basename "$0") 1.2.3                                 # Build with tag '1.2.3' for prod env
    $(basename "$0") 1.2.3 --push                          # Build and push with tag '1.2.3'
    $(basename "$0") 1.2.3 --env=staging                   # Build for staging environment
    $(basename "$0") 1.2.3 --platform=linux/amd64          # Build for AMD64 platform
    $(basename "$0") 1.0 --push --env=dev --platform=linux/amd64  # Build dev, push for specific platform

The built image will be named: ${IMAGE_NAME}:TAG
After build, the tag will be written to version.txt file.
EOF
}

# Check if no arguments provided or help requested
if [ $# -eq 0 ] || [ "$1" == "--help" ] || [ "$1" == "-h" ]; then
    show_help
    exit 0
fi

# First argument is always the TAG
TAG="$1"
shift

# Parse remaining arguments (options)
while [ $# -gt 0 ]; do
    case $1 in
        --help|-h)
        show_help
        exit 0
        ;;
        --platform=*)
        PLATFORM_ARG="$1"
        shift
        ;;
        --env=*)
        ENV="${1#--env=}"
        shift
        ;;
        --push)
        PUSH=true
        shift
        ;;
        *)
        echo "Error: Unknown option '$1'"
        echo "Use --help to see available options."
        exit 1
        ;;
    esac
done

echo "[+] Using image tag: $TAG"
echo "[+] Using environment: $ENV"

ENV_FILE=".env.${ENV}"

# Extract VITE_ variables from environment file
rm -f "$BUILD_ENV_FILE"
echo "[+] Extracting VITE_ vars from $ENV_FILE..."
grep '^VITE_' "$ENV_FILE" > "$BUILD_ENV_FILE"

# Build the image without cache (always fresh build)
echo "[+] Building Docker image with tag: $TAG (no cache)..."
docker build --build-arg BUILD_ENV_FILE=$BUILD_ENV_FILE --no-cache $PLATFORM_ARG -t "${IMAGE_NAME}:${TAG}" .

echo "[+] Image built successfully"
echo "[+] Tag: ${IMAGE_NAME}:${TAG}"

# Push the image if requested
if [ "$PUSH" == true ]; then
    echo "[+] Checking Docker Hub connectivity..."
    if docker info > /dev/null 2>&1 && docker login --help > /dev/null 2>&1; then
        echo "[+] Pushing ${IMAGE_NAME}:${TAG}..."
        if docker push "${IMAGE_NAME}:${TAG}"; then
            echo "[+] Image pushed successfully"
        else
            echo "[-] Failed to push image to Docker Hub"
            exit 1
        fi
    else
        echo "[-] Docker Hub not available or not logged in. Skipping push."
        echo "    Run 'docker login' to authenticate with Docker Hub"
        exit 1
    fi
else
    echo "[+] Skipping Docker Hub push (use --push to enable)"
fi

# Write the tag to version.txt
echo "[+] Writing tag ${TAG} to version.txt..."
echo "${TAG}" > version.txt

echo "[+] Done."
