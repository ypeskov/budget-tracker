#!/usr/bin/env bash

build_and_tag() {
    local tag="latest"
    local platform_option=""

    for arg in "$@"; do
        if [[ $arg == --platform=* ]]; then
            platform_option=$arg
        elif [[ $arg != "push" ]]; then
            tag=$arg
        fi
    done

    local build_command="docker build --target prod "
    
    [[ -z "$platform_option" ]] && platform_option="--platform=linux/arm64"
    build_command+="--no-cache $platform_option"

    build_command+=" -t ypeskov/api-orgfin:$tag ."

    eval "$build_command"
    echo "$tag" > version.txt
}

if [[ $# -eq 0 ]]; then
    # shellcheck disable=SC2164
    cd back-fastapi
    build_and_tag
elif [[ $1 == "push" ]]; then
    # shellcheck disable=SC2164
    cd back-fastapi
    build_and_tag "${@:2}"
    docker push ypeskov/api-orgfin:${2:-latest}

    echo "Updating docker-compose.yaml"
    sed -i '' "s|ypeskov/api-orgfin:[^[:space:]]*|ypeskov/api-orgfin:${2:-latest}|g" ../docker-compose.prod.yml
    echo "Updated docker-compose.prod.yaml: $(grep -o "ypeskov/api-orgfin:[^[:space:]]*" ../docker-compose.prod.yml)"
    echo "=================================== ATTENTION ==================================="
    echo "Commit to git and push to GitHub to apply changes."
    echo "Run deploy_full.sh on the server to apply changes."

    echo "${2:-latest}" > version.txt
else
    echo "Usage:"
    echo "$0                                           # Build and tag :latest"
    echo "$0 push                                      # Build, tag and push :latest to Docker Hub"
    echo "$0 push <tag>                                # Build, tag as <tag> and push to Docker Hub"
    echo "$0 push [--platform=<platform>]              # Build for optional platform, tag as :latest, and push to Docker Hub"
    echo "$0 push <tag> [--platform=<platform>]        # Build for optional platform, tag as <tag>, and push to Docker Hub"
fi
