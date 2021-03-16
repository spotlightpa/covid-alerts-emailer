#!/bin/bash

set -euxo pipefail

# Get the directory that this script file is in
THIS_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)

cd "$THIS_DIR"

echo "Using $(which python3) for setup"
python3 -m venv --clear venv
venv/bin/pip install --upgrade pip
venv/bin/pip install --no-deps -r requirements/prod.txt
venv/bin/python3 -m compileall venv -q
