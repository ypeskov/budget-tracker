#!/usr/bin/env bash

sudo supervisorctl update

sudo supervisorctl restart fastapi-app

sudo supervisorctl status
