"""Стартовый скрипт использует тот же исполнитель, что и ручной ввод."""

from pathlib import Path

from shell import Result, Shell


def script_events(shell: Shell, path: Path):
    try:
        lines = path.read_text(encoding="utf-8-sig").splitlines()
    except (OSError, UnicodeError) as exc:
        yield "", Result(f"Ошибка: не удалось прочитать стартовый скрипт {path}: {exc}\n", error=True)
        return
    for number, line in enumerate(lines, start=1):
        if not line.strip():
            continue
        entered = shell.prompt + line + "\n"
        result = shell.execute(line)
        if result.error:
            result.output = f"{path}:{number}: {result.output}"
        yield entered, result
        if result.exit:
            return
