#!/bin/bash

set -euxo pipefail

# Get the directory that this script file is in
THIS_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)

cd "$THIS_DIR"

[[ -f .env ]] && set +x && echo "sourcing .env" && source .env || echo "No .env file found"
set -x

venv/bin/python -m src.covid_email_alerts
