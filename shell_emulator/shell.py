"""Разбор строки и исполнение команд без привязки к GUI."""

from dataclasses import dataclass
from pathlib import Path

from vfs import VFS, VFSError


class ShellError(Exception):
    """Ожидаемая ошибка команды, которую нужно показать пользователю."""


@dataclass
class Result:
    output: str = ""
    clear: bool = False
    exit: bool = False
    error: bool = False


def parse_command(line: str) -> tuple[str, list[str]]:
    parts = line.split()
    return (parts[0], parts[1:]) if parts else ("", [])


class Shell:
    def __init__(self, vfs=None):
        self.vfs = vfs if vfs is not None else VFS()
        self.cwd = "/"

    @property
    def prompt(self) -> str:
        return f"student@vfs:{self.cwd}$ "

    def execute(self, line: str) -> Result:
        command, args = parse_command(line)
        if not command:
            return Result()
        try:
            if command == "exit":
                if args:
                    raise ShellError("exit: аргументы не поддерживаются")
                return Result(exit=True)
            if command == "vfs-save":
                if len(args) != 1:
                    raise ShellError("vfs-save: ожидается один путь в файловой системе ОС")
                self.vfs.save(Path(args[0]))
                return Result(f"VFS сохранена: {args[0]}\n")
            if command in ("ls", "cd"):
                if len(args) > 1:
                    raise ShellError(f"{command}: ожидается не более одного пути")
                return Result(f"{command}: аргументы: {' '.join(args)}\n")
            raise ShellError(f"{command}: неизвестная команда")
        except (ShellError, VFSError) as exc:
            return Result(f"Ошибка: {exc}\n", error=True)
