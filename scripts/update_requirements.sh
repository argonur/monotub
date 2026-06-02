#!/usr/bin/env bash

set -e

source .venv/bin/activate
pip install --upgrade pip pip-tools
pip-compile pyproject.toml --extra dev --no-strip-extras -o requirements.txt
