import tempfile
import unittest
from pathlib import Path

from config import parse_args
from shell import Shell
from startup import script_events


class ConfigurationTests(unittest.TestCase):
    def test_defaults(self):
        config = parse_args([])
        self.assertEqual(config.vfs.name, "demo.csv")
        self.assertIsNone(config.script)

    def test_custom_paths(self):
        config = parse_args(["--vfs", "my disk.csv", "--script", "start.txt"])
        self.assertEqual(config.vfs, Path("my disk.csv"))
        self.assertEqual(config.script, Path("start.txt"))


class StartupTests(unittest.TestCase):
    def test_errors_do_not_stop_script_but_exit_does(self):
        with tempfile.TemporaryDirectory() as directory:
            script = Path(directory) / "start.txt"
            script.write_text("\nls\nunknown\ncd a b\nls /\nexit\nnever\n", encoding="utf-8")
            events = list(script_events(Shell(), script))
        self.assertEqual(len(events), 5)
        self.assertTrue(events[1][1].error)
        self.assertIn(":3:", events[1][1].output)
        self.assertTrue(events[2][1].error)
        self.assertFalse(events[3][1].error)
        self.assertTrue(events[4][1].exit)
        self.assertIn("$ ls", events[0][0])

    def test_missing_script(self):
        events = list(script_events(Shell(), Path("/missing/script.txt")))
        self.assertEqual(len(events), 1)
        self.assertTrue(events[0][1].error)
        self.assertIn("стартовый скрипт", events[0][1].output)

    def test_bad_encoding(self):
        with tempfile.TemporaryDirectory() as directory:
            script = Path(directory) / "bad.txt"
            script.write_bytes(b"\xff")
            self.assertTrue(list(script_events(Shell(), script))[0][1].error)
