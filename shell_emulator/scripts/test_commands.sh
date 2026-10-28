#!/bin/sh
# Закройте первое окно, чтобы открыть демонстрацию mv.
set -eu
cd "$(dirname "$0")/.."
PYTHON=${PYTHON:-python3}
mkdir -p output
"$PYTHON" main.py --vfs examples/vfs/demo.csv --script examples/startup/stage4.txt
"$PYTHON" main.py --vfs examples/vfs/demo.csv --script examples/startup/stage5.txt
