import base64
import csv
import tempfile
import unittest
from pathlib import Path

from shell import Shell
from vfs import VFS, VFSError


class VFSTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.source = Path(self.temp.name) / "disk.csv"

    def write(self, rows):
        with self.source.open("w", encoding="utf-8", newline="") as stream:
            writer = csv.writer(stream)
            writer.writerow(["path", "type", "content"])
            writer.writerows(rows)

    def test_empty_and_nested_binary_round_trip(self):
        self.write([])
        self.assertEqual(set(VFS.load(self.source).nodes), {"/"})
        data = b"\x00\xff\xfe\n"
        self.write([
            ["/a/b/c/data.bin", "file", base64.b64encode(data).decode()],
            ["/a/b/c", "dir", ""], ["/a", "dir", ""], ["/a/b", "dir", ""],
        ])
        original = self.source.read_bytes()
        vfs = VFS.load(self.source)
        self.assertEqual(vfs.nodes["/a/b/c/data.bin"].data, data)
        target = Path(self.temp.name) / "saved.csv"
        vfs.save(target)
        self.assertEqual(VFS.load(target).nodes, vfs.nodes)
        self.assertEqual(self.source.read_bytes(), original)

    def test_invalid_rows(self):
        cases = [
            [["relative", "dir", ""]],
            [["/a/../b", "dir", ""]],
            [["//a", "dir", ""]],
            [["/a/", "dir", ""]],
            [["/", "file", ""]],
            [["/a", "dir", "text"]],
            [["/a", "other", ""]],
            [["/a", "file", "!not-base64!"]],
            [["/a", "dir", ""], ["/a", "dir", ""]],
            [["/a/b", "file", ""]],
            [["/a", "file", ""], ["/a/b", "file", ""]],
            [["/a", "file"]],
            [["/a", "file", "", "extra"]],
        ]
        for rows in cases:
            with self.subTest(rows=rows):
                self.write(rows)
                with self.assertRaises(VFSError):
                    VFS.load(self.source)

    def test_missing_bad_header_and_encoding(self):
        with self.assertRaises(VFSError):
            VFS.load(self.source)
        for content in (b"wrong,header\n", b"\xff", b'path,type,content\n"/a,dir,\n'):
            self.source.write_bytes(content)
            with self.subTest(content=content), self.assertRaises(VFSError):
                VFS.load(self.source)

    def test_save_command_and_errors(self):
        shell = Shell(VFS())
        target = Path(self.temp.name) / "saved.csv"
        self.assertFalse(shell.execute(f"vfs-save {target}").error)
        self.assertEqual(set(VFS.load(target).nodes), {"/"})
        for command in ("vfs-save", "vfs-save a b", f"vfs-save {target}/bad"):
            with self.subTest(command=command):
                self.assertTrue(shell.execute(command).error)
