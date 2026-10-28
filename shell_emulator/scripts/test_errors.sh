#!/bin/sh
# Ошибочные запуски; после проверки закрывайте каждое окно.
set -eu
cd "$(dirname "$0")/.."
PYTHON=${PYTHON:-python3}
"$PYTHON" main.py --vfs examples/vfs/demo.csv --script examples/startup/missing.txt
"$PYTHON" main.py --vfs examples/vfs/missing.csv --script examples/startup/stage2.txt
"$PYTHON" main.py --vfs examples/vfs/invalid.csv --script examples/startup/stage2.txt
