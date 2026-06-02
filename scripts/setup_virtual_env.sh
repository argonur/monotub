#!/bin/bash

set -e

echo "Creating Virtual Environment"
python3 -m venv .venv
echo "Activating Virtual Environment"
source .venv/bin/activate
echo "Install needed packages"
pip install -e ".[dev]"