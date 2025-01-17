#!/usr/bin/env bash

PYTHONPATH=$(pwd):$PYTHONPATH

export PYTHONPATH

python -m app.data_loaders.test_data.clear_test_db
