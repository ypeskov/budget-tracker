#!/usr/bin/env bash

source venv/bin/activate

export PYTHONPATH=$(pwd):$PYTHONPATH

pytest --cov-report term-missing --cov=app app/tests/ -s
