#!/usr/bin/env bash

export PYTHONPATH=$(pwd):$PYTHONPATH

pytest --cov-report term-missing --cov=app app/tests/ -s
