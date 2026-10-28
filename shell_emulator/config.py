"""Параметры реальной командной строки ОС."""

import argparse
from pathlib import Path


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description="GUI-эмулятор UNIX-подобной оболочки")
    parser.add_argument(
        "--vfs", type=Path,
        default=Path(__file__).resolve().parent / "examples/vfs/demo.csv",
        help="путь к CSV-файлу виртуальной файловой системы",
    )
    parser.add_argument("--script", type=Path, help="путь к стартовому скрипту UTF-8")
    return parser.parse_args(argv)
