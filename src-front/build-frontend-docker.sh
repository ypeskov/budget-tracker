#!/usr/bin/env bash
set -e

ENV="prod"
ENV_FILE=""
BUILD_ENV_FILE=".env.build"

for arg in "$@"; do
    if [[ $arg == --env=* ]]; then
        ENV="${arg#--env=}"
    fi
done

IMAGE_TAG="${1:-latest}"
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

update_kubernetes_deployment() {
    local tag=$1
    sed -i "" "s|ypeskov/frontend-orgfin:[^[:space:]]*|ypeskov/frontend-orgfin:${tag}|g" ../Kubernetes/orgfin-frontend/base/deployment.yaml
}

echo "[+] Building Docker image with tag: $IMAGE_TAG"
build_and_tag $IMAGE_TAG
update_kubernetes_deployment $IMAGE_TAG

echo "[+] Image built successfully"
echo "[+] Tag: ypeskov/frontend-orgfin:$IMAGE_TAG"
echo "[+] Pushing to Docker Hub..."
docker push "ypeskov/frontend-orgfin:$IMAGE_TAG"
echo "[+] Image pushed successfully"