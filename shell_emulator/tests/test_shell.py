import unittest

from shell import Shell, parse_command


class ReplTests(unittest.TestCase):
    def setUp(self):
        self.shell = Shell()

    def test_parser_splits_whitespace(self):
        self.assertEqual(parse_command("  ls   one\ttwo  "), ("ls", ["one", "two"]))
        self.assertEqual(parse_command("  "), ("", []))

    def test_empty_input(self):
        self.assertEqual(self.shell.execute(" ").output, "")

    def test_stubs(self):
        self.assertEqual(self.shell.execute("ls /tmp").output, "ls: аргументы: /tmp\n")
        self.assertEqual(self.shell.execute("cd /home").output, "cd: аргументы: /home\n")

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
