#!/usr/bin/env bash

source ../venv/bin/activate

sudo supervisorctl update

sudo supervisorctl restart fastapi-app

sudo supervisorctl status
