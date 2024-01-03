#!/usr/bin/env bash

export PYTHONPATH=$(pwd):$PYTHONPATH

python -m app.data_loaders.test_data.clear_test_db
