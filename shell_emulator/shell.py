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
            if command == "ls":
                show_hidden = "-a" in args
                paths = [arg for arg in args if arg != "-a"]
                if args.count("-a") > 1 or len(paths) > 1 or any(arg.startswith("-") for arg in paths):
                    raise ShellError("ls: использование: ls [-a] [путь]")
                path = self.vfs.resolve(paths[0] if paths else ".", self.cwd)
                names = self.vfs.list_directory(path, show_hidden)
                return Result("".join(name + "\n" for name in names))
            if command == "cd":
                if len(args) > 1:
                    raise ShellError(f"{command}: ожидается не более одного пути")
                path = self.vfs.resolve(args[0] if args else "/", self.cwd)
                if self.vfs.nodes[path].kind != "dir":
                    raise ShellError(f"cd: не каталог: {path}")
                self.cwd = path
                return Result()
            if command == "echo":
                no_newline = bool(args and args[0] == "-n")
                text = " ".join(args[1:] if no_newline else args)
                return Result(text + ("" if no_newline else "\n"))
            if command == "clear":
                if args:
                    raise ShellError("clear: аргументы не поддерживаются")
                return Result(clear=True)
            if command == "rev":
                if not args:
                    raise ShellError("rev: ожидается хотя бы один путь к текстовому файлу")
                output = []
                for arg in args:
                    text = self.vfs.read_text(self.vfs.resolve(arg, self.cwd))
                    for line in text.splitlines(keepends=True):
                        body = line.rstrip("\r\n")
                        output.append(body[::-1] + line[len(body):])
                return Result("".join(output))
            raise ShellError(f"{command}: неизвестная команда")
        except (ShellError, VFSError) as exc:
            return Result(f"Ошибка: {exc}\n", error=True)
