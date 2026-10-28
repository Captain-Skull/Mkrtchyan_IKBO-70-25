import unittest
from pathlib import Path

from shell import Shell, parse_command
from vfs import VFS


class ReplTests(unittest.TestCase):
    def setUp(self):
        self.shell = Shell()

    def test_parser_splits_whitespace(self):
        self.assertEqual(parse_command("  ls   one\ttwo  "), ("ls", ["one", "two"]))
        self.assertEqual(parse_command("  "), ("", []))

    def test_empty_input(self):
        self.assertEqual(self.shell.execute(" ").output, "")

    def test_ls_and_cd_on_empty_vfs(self):
        self.assertEqual(self.shell.execute("ls").output, "")
        self.assertFalse(self.shell.execute("cd /").error)

    def test_unknown_command(self):
        result = self.shell.execute("missing")
        self.assertTrue(result.error)
        self.assertIn("неизвестная команда", result.output)

    def test_exit_arguments(self):
        self.assertTrue(self.shell.execute("exit extra").error)
        self.assertFalse(self.shell.execute("exit extra").exit)
        self.assertTrue(self.shell.execute("exit").exit)

    def test_bad_stub_arguments(self):
        self.assertTrue(self.shell.execute("cd a b").error)
        self.assertTrue(self.shell.execute("ls a b").error)


if __name__ == "__main__":
    unittest.main()


class CommandTests(unittest.TestCase):
    def setUp(self):
        self.shell = Shell(VFS.load(Path(__file__).resolve().parents[1] / "examples/vfs/demo.csv"))

    def test_ls_directory_file_and_hidden(self):
        result = self.shell.execute("ls")
        self.assertFalse(result.error)
        self.assertIn("home/\n", result.output)
        self.assertNotIn(".hidden", result.output)
        self.assertIn(".hidden\n", self.shell.execute("ls -a /").output)
        self.assertIn("../\n", self.shell.execute("ls -a").output)
        self.assertEqual(self.shell.execute("ls /hello.txt").output, "hello.txt\n")
        self.assertEqual(self.shell.execute("ls /tmp").output, "")

    def test_cd_and_relative_paths(self):
        self.assertFalse(self.shell.execute("cd /home/student/docs").error)
        self.assertEqual(self.shell.cwd, "/home/student/docs")
        self.assertIn("readme.txt", self.shell.execute("ls .").output)
        self.shell.execute("cd ..")
        self.assertEqual(self.shell.cwd, "/home/student")
        self.shell.execute("cd ./docs/../..")
        self.assertEqual(self.shell.cwd, "/home")
        self.shell.execute("cd")
        self.assertEqual(self.shell.cwd, "/")
        self.shell.execute("cd ../../..")
        self.assertEqual(self.shell.cwd, "/")
        self.assertIn(":/$ ", self.shell.prompt)

    def test_invalid_paths_leave_cwd_unchanged(self):
        for command in ("cd /hello.txt", "ls /missing", "cd /missing", "ls /hello.txt/..", "ls /hello.txt/", "ls /missing/../home"):
            with self.subTest(command=command):
                self.assertTrue(self.shell.execute(command).error)
                self.assertEqual(self.shell.cwd, "/")

    def test_rev_unicode_multiple_empty_and_binary(self):
        self.assertEqual(self.shell.execute("rev /hello.txt").output, "!XINU ,olleH\n")
        self.assertEqual(self.shell.execute("rev /empty.txt /hello.txt").output, "!XINU ,olleH\n")
        self.assertEqual(self.shell.execute("rev /home/student/docs/readme.txt").output, "!рим ,тевирП\nSFV и nohtyP\n")
        for command in ("rev", "rev /binary.bin", "rev /tmp", "rev /missing"):
            with self.subTest(command=command):
                self.assertTrue(self.shell.execute(command).error)

    def test_echo_and_clear(self):
        self.assertEqual(self.shell.execute("echo  hello   world").output, "hello world\n")
        self.assertEqual(self.shell.execute("echo").output, "\n")
        self.assertEqual(self.shell.execute("echo -n hello").output, "hello")
        self.assertEqual(self.shell.execute("echo -n").output, "")
        self.assertTrue(self.shell.execute("clear").clear)
        self.assertTrue(self.shell.execute("clear x").error)

    def test_bad_ls_options(self):
        for command in ("ls -l", "ls -a / /home", "ls -a -a"):
            with self.subTest(command=command):
                self.assertTrue(self.shell.execute(command).error)
