#!/bin/bash
set -euo pipefail

git pull
kubectl apply -k overlays/prod