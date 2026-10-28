"""Проверки реального Tk GUI: python3 -m tests.gui_smoke (нужен экран)."""

import os
import tempfile
import tkinter as tk
import unittest
from pathlib import Path
from types import SimpleNamespace

from gui import Terminal


PROJECT = Path(__file__).resolve().parents[1]


class GuiTests(unittest.TestCase):
    def open_terminal(self, vfs=None, script=None):
        root = tk.Tk()
        root.withdraw()
        self.addCleanup(self.close_root, root)
        terminal = Terminal(root, SimpleNamespace(
            vfs=vfs or PROJECT / "examples/vfs/demo.csv", script=script,
        ))
        return root, terminal

    @staticmethod
    def close_root(root):
        try:
            root.destroy()
        except tk.TclError:
            pass  # exit уже уничтожил окно.

    def finish_script(self, root, terminal):
        timed_out = []

        def timeout():
            timed_out.append(True)
            root.quit()

        def poll():
            if str(terminal.entry["state"]) == "normal":
                root.quit()
            else:
                root.after(20, poll)

        timer = root.after(5000, timeout)
        root.after(20, poll)
        root.mainloop()
        root.after_cancel(timer)
        self.assertFalse(timed_out, "стартовый скрипт не завершился")

    def test_interactive_input_clear_and_exit(self):
        root, terminal = self.open_terminal()
        self.assertIn("demo.csv", root.title())
        for line in ("cd /home/student", "ls", "unknown"):
            terminal.entry.insert(0, line)
            terminal.submit()
        text = terminal.output.get("1.0", "end")
        self.assertIn("[config] VFS:", text)
        self.assertIn("notes.txt", text)
        self.assertIn("неизвестная команда", text)
        self.assertIn("/home/student$", terminal.prompt["text"])
        terminal.entry.insert(0, "clear")
        terminal.submit()
        self.assertEqual(terminal.output.get("1.0", "end-1c"), "")
        self.assertEqual(terminal.shell.cwd, "/home/student")
        terminal.entry.insert(0, "exit")
        terminal.submit()
        with self.assertRaises(tk.TclError):
            root.winfo_exists()

    def test_invalid_vfs_disables_input(self):
        for name in ("invalid.csv", "missing.csv"):
            with self.subTest(name=name):
                root, terminal = self.open_terminal(PROJECT / "examples/vfs" / name)
                self.assertEqual(str(terminal.entry["state"]), "disabled")
                self.assertIn("Ошибка загрузки VFS", terminal.output.get("1.0", "end"))
                root.destroy()

    def test_missing_script_allows_interactive_input(self):
        root, terminal = self.open_terminal(script=PROJECT / "examples/startup/missing.txt")
        self.finish_script(root, terminal)
        self.assertIn("стартовый скрипт", terminal.output.get("1.0", "end"))

    def test_full_startup_and_saved_state(self):
        with tempfile.TemporaryDirectory() as directory:
            old_cwd = Path.cwd()
            try:
                os.chdir(directory)
                Path("output").mkdir()
                root, terminal = self.open_terminal(script=PROJECT / "examples/startup/all.txt")
                self.finish_script(root, terminal)
                text = terminal.output.get("1.0", "end")
                self.assertIn("Скрипт завершён", text)
                self.assertIn("неизвестная команда", text)
                self.assertTrue(Path("output/demo-saved.csv").is_file())
                self.assertIn("/archive/student/docs/readme.txt", terminal.shell.vfs.nodes)
            finally:
                os.chdir(old_cwd)

    def test_exit_in_startup_closes_window(self):
        root, terminal = self.open_terminal(script=PROJECT / "examples/startup/exit.txt")
        root.after(5000, root.quit)
        root.mainloop()
        with self.assertRaises(tk.TclError):
            terminal.entry.get()


if __name__ == "__main__":
    unittest.main(verbosity=2)
