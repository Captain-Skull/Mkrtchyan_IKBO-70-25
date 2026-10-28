"""CSV хранится на диске; после загрузки дерево существует только в памяти."""

import base64
import binascii
import csv
import posixpath
from dataclasses import dataclass
from pathlib import Path


class VFSError(Exception):
    """Ошибка формата, доступа или операции с виртуальным деревом."""


@dataclass(frozen=True)
class Node:
    kind: str
    data: bytes = b""


class VFS:
    def __init__(self):
        self.nodes = {"/": Node("dir")}

    @classmethod
    def load(cls, source: Path):
        vfs = cls()
        seen = set()
        try:
            with source.open(encoding="utf-8-sig", newline="") as stream:
                reader = csv.DictReader(stream, strict=True)
                if reader.fieldnames != ["path", "type", "content"]:
                    raise VFSError("ожидается заголовок path,type,content")
                for row in reader:
                    path, kind, content = row["path"], row["type"], row["content"]
                    if None in row or None in (path, kind, content):
                        raise VFSError(f"строка {reader.line_num}: нужно ровно три поля")
                    if (
                        not path.startswith("/") or path.startswith("//")
                        or posixpath.normpath(path) != path or "\x00" in path
                    ):
                        raise VFSError(f"некорректный абсолютный путь: {path!r}")
                    if path in seen:
                        raise VFSError(f"повторяющийся путь: {path}")
                    if kind not in ("dir", "file") or (path == "/" and kind != "dir"):
                        raise VFSError(f"неверный тип узла: {path}")
                    if kind == "dir" and content:
                        raise VFSError(f"каталог не должен содержать данные: {path}")
                    try:
                        data = base64.b64decode(content, validate=True) if kind == "file" else b""
                    except (binascii.Error, ValueError) as exc:
                        raise VFSError(f"неверный base64: {path}") from exc
                    vfs.nodes[path] = Node(kind, data)
                    seen.add(path)
        except (OSError, UnicodeError, csv.Error) as exc:
            raise VFSError(f"не удалось загрузить {source}: {exc}") from exc
        for path in vfs.nodes:
            if path != "/":
                parent = vfs.nodes.get(posixpath.dirname(path))
                if parent is None or parent.kind != "dir":
                    raise VFSError(f"отсутствует родительский каталог: {path}")
        return vfs

    def save(self, target: Path):
        try:
            with target.open("w", encoding="utf-8", newline="") as stream:
                writer = csv.writer(stream)
                writer.writerow(["path", "type", "content"])
                for path, node in sorted(self.nodes.items()):
                    content = base64.b64encode(node.data).decode("ascii") if node.kind == "file" else ""
                    writer.writerow([path, node.kind, content])
        except OSError as exc:
            raise VFSError(f"не удалось сохранить {target}: {exc}") from exc
