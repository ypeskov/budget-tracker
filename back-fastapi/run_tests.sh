#!/usr/bin/env bash

OLD_PYTHONPATH=$PYTHONPATH
export PYTHONPATH=$(pwd):$PYTHONPATH
export TEST_MODE=True

pytest --cov-report term-missing --cov=app app/tests/ -s

unset TEST_MODE
export PYTHONPATH=$OLD_PYTHONPATH
