import tempfile
import unittest
from pathlib import Path

from shell import Shell
from vfs import VFS


class MoveTests(unittest.TestCase):
    def setUp(self):
        self.source = Path(__file__).resolve().parents[1] / "examples/vfs/demo.csv"
        self.original = self.source.read_bytes()
        self.shell = Shell(VFS.load(self.source))

    def test_rename_and_move_into_directory(self):
        self.assertFalse(self.shell.execute("mv /hello.txt /greeting.txt").error)
        self.assertNotIn("/hello.txt", self.shell.vfs.nodes)
        self.assertFalse(self.shell.execute("mv /greeting.txt /tmp").error)
        self.assertEqual(self.shell.vfs.nodes["/tmp/greeting.txt"].data, b"Hello, UNIX!\n")
        self.assertEqual(self.source.read_bytes(), self.original)

    def test_move_subtree_updates_cwd(self):
        self.shell.execute("cd /home/student/docs")
        self.assertFalse(self.shell.execute("mv /home/student /archive").error)
        self.assertEqual(self.shell.cwd, "/archive/student/docs")
        self.assertEqual(self.shell.execute("ls").output, "readme.txt\n")
        self.assertNotIn("/home/student/docs/readme.txt", self.shell.vfs.nodes)
        self.assertIn("/archive/student/docs/readme.txt", self.shell.vfs.nodes)
        self.assertFalse(self.shell.execute("mv /archive /backup").error)
        self.assertEqual(self.shell.cwd, "/backup/student/docs")

    def test_replace_file_and_binary_integrity(self):
        self.assertFalse(self.shell.execute("mv /binary.bin /empty.txt").error)
        self.assertEqual(self.shell.vfs.nodes["/empty.txt"].data, b"\x00\xff\x80")
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "saved.csv"
            self.assertFalse(self.shell.execute(f"vfs-save {target}").error)
            self.assertEqual(VFS.load(target).nodes, self.shell.vfs.nodes)

    def test_replace_empty_directory(self):
        self.shell.execute("mv /tmp /archive/student")
        self.assertFalse(self.shell.execute("mv /home/student /archive").error)
        self.assertIn("/archive/student/docs/readme.txt", self.shell.vfs.nodes)

    def test_errors_preserve_tree_and_cwd(self):
        commands = [
            "mv", "mv /hello.txt", "mv a b c", "mv /missing /tmp",
            "mv / /root", "mv /home /home/student/docs",
            "mv /home /home", "mv /hello.txt /hello.txt", "mv /hello.txt /",
            "mv /home /empty.txt",
            "mv /hello.txt /missing/file", "mv /hello.txt /missing/",
            "mv /hello.txt /binary.bin/child", "mv /hello.txt/ /tmp",
        ]
        for command in commands:
            with self.subTest(command=command):
                before = dict(self.shell.vfs.nodes)
                cwd = self.shell.cwd
                result = self.shell.execute(command)
                self.assertTrue(result.error, result.output)
                self.assertEqual(self.shell.vfs.nodes, before)
                self.assertEqual(self.shell.cwd, cwd)

    def test_nonempty_directory_collision(self):
        self.assertFalse(self.shell.execute("mv /home/student /archive").error)
        self.assertFalse(self.shell.execute("mv /home /tmp/student").error)
        before = dict(self.shell.vfs.nodes)
        result = self.shell.execute("mv /tmp/student /archive")
        self.assertTrue(result.error)
        self.assertIn("не пуст", result.output)
        self.assertEqual(self.shell.vfs.nodes, before)

    def test_file_cannot_replace_directory_inside_destination(self):
        self.assertFalse(self.shell.execute("mv /tmp /archive/hello.txt").error)
        before = dict(self.shell.vfs.nodes)
        self.assertTrue(self.shell.execute("mv /hello.txt /archive").error)
        self.assertEqual(self.shell.vfs.nodes, before)
