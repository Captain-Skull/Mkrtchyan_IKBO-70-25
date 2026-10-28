#!/bin/sh
set -eu
cd "$(dirname "$0")/.."
PYTHON=${PYTHON:-python3}
mkdir -p output
exec "$PYTHON" main.py --vfs examples/vfs/demo.csv --script examples/startup/all.txt
