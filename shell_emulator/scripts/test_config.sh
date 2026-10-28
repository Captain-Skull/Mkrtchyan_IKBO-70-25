#!/bin/sh
# Закрывайте окно, чтобы перейти к следующему запуску.
set -eu
cd "$(dirname "$0")/.."
PYTHON=${PYTHON:-python3}
"$PYTHON" main.py
"$PYTHON" main.py --vfs examples/vfs/demo.csv
"$PYTHON" main.py --script examples/startup/stage2.txt
"$PYTHON" main.py --vfs examples/vfs/demo.csv --script examples/startup/stage2.txt
