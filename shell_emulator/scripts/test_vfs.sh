#!/bin/sh
# Три варианта VFS; закрывайте каждое окно после просмотра.
set -eu
cd "$(dirname "$0")/.."
PYTHON=${PYTHON:-python3}
mkdir -p output
"$PYTHON" main.py --vfs examples/vfs/minimal.csv --script examples/startup/stage3.txt
"$PYTHON" main.py --vfs examples/vfs/files.csv --script examples/startup/stage3.txt
"$PYTHON" main.py --vfs examples/vfs/demo.csv --script examples/startup/stage3.txt
