#!/usr/bin/env bash
set -e

ENV="prod"
ENV_FILE=""
BUILD_ENV_FILE=".env.build"
PUSH_TO_HUB=false

show_help() {
    cat << EOF
Usage: $0 [IMAGE_TAG] [OPTIONS]

Build Docker image for frontend application.

ARGUMENTS:
    IMAGE_TAG           Docker image tag (default: latest)

OPTIONS:
    --env=ENV          Environment to use (default: prod)
    --push             Push image to Docker Hub after building
    --help             Show this help message

EXAMPLES:
    $0                          Build with latest tag
    $0 v1.2.3                   Build with specific tag
    $0 --push                   Build and push to Docker Hub
    $0 v1.2.3 --env=staging     Build with staging env and v1.2.3 tag
    $0 --env=staging --push     Build staging env and push to Docker Hub

EOF
}

# Parse arguments
IMAGE_TAG="latest"
for arg in "$@"; do
    if [[ $arg == --env=* ]]; then
        ENV="${arg#--env=}"
    elif [[ $arg == "--push" ]]; then
        PUSH_TO_HUB=true
    elif [[ $arg == "--help" ]]; then
        show_help
        exit 0
    elif [[ $arg != --* ]]; then
        IMAGE_TAG="$arg"
    fi
done
echo "[+] Using image tag: $IMAGE_TAG"
echo "[+] Using environment: $ENV"

ENV_FILE=".env.${ENV}"

rm -f "$BUILD_ENV_FILE"
echo "[+] Extracting VITE_ vars from $ENV_FILE..."
grep '^VITE_' "$ENV_FILE" > "$BUILD_ENV_FILE"

build_and_tag() {
    local tag=$1
    local platform_option="--platform=linux/arm64"
    local build_command="docker build --build-arg BUILD_ENV_FILE=$BUILD_ENV_FILE "
    build_command+=" --no-cache $platform_option"
    build_command+=" -t ypeskov/frontend-orgfin:$tag ."
    echo "$build_command"
    eval "$build_command"
    echo "$tag" > version.txt
}

echo "[+] Building Docker image with tag: $IMAGE_TAG"
build_and_tag $IMAGE_TAG

echo "[+] Image built successfully"
echo "[+] Tag: ypeskov/frontend-orgfin:$IMAGE_TAG"

if [[ $PUSH_TO_HUB == true ]]; then
    echo "[+] Checking Docker Hub connectivity..."
    if docker info > /dev/null 2>&1 && docker login --help > /dev/null 2>&1; then
        echo "[+] Pushing to Docker Hub..."
        if docker push "ypeskov/frontend-orgfin:$IMAGE_TAG"; then
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