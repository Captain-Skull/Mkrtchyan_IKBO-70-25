"""Окно терминала; команды исполняет независимый объект Shell."""

import tkinter as tk
from tkinter.scrolledtext import ScrolledText

from shell import Shell
from startup import script_events


class Terminal:
    def __init__(self, root: tk.Tk, config):
        self.root = root
        self.shell = Shell()
        root.title(f"Эмулятор оболочки — {config.vfs.name}")
        root.geometry("920x580")
        self.output = ScrolledText(
            root, wrap=tk.WORD, font=("Courier", 13),
            bg="#18212b", fg="#e6edf3", insertbackground="white",
            state=tk.DISABLED, padx=12, pady=12,
        )
        self.output.pack(fill=tk.BOTH, expand=True)
        row = tk.Frame(root)
        row.pack(fill=tk.X, padx=10, pady=10)
        self.prompt = tk.Label(row, text=self.shell.prompt, font=("Courier", 12))
        self.prompt.pack(side=tk.LEFT)
        self.entry = tk.Entry(row, font=("Courier", 13))
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.entry.bind("<Return>", self.submit)
        self.write("Эмулятор оболочки. Для завершения введите exit.\n")
        self.write(f"[config] VFS: {config.vfs.resolve()}\n")
        self.write(f"[config] Стартовый скрипт: {config.script.resolve() if config.script else 'не задан'}\n")
        self.entry.focus_set()
        if config.script:
            self.entry.configure(state=tk.DISABLED)
            self.events = iter(script_events(self.shell, config.script))
            root.after(100, self.script_step)

    def script_step(self):
        try:
            entered, result = next(self.events)
        except StopIteration:
            self.entry.configure(state=tk.NORMAL)
            self.entry.focus_set()
            return
        self.write(entered)
        self.apply(result)
        if not result.exit:
            self.root.after(40, self.script_step)

    def write(self, text: str):
        self.output.configure(state=tk.NORMAL)
        self.output.insert(tk.END, text)
        self.output.see(tk.END)
        self.output.configure(state=tk.DISABLED)

    def submit(self, event=None):
        line = self.entry.get()
        self.entry.delete(0, tk.END)
        self.write(self.shell.prompt + line + "\n")
        self.apply(self.shell.execute(line))

    def apply(self, result):
        if result.clear:
            self.output.configure(state=tk.NORMAL)
            self.output.delete("1.0", tk.END)
            self.output.configure(state=tk.DISABLED)
        self.write(result.output)
        self.prompt.configure(text=self.shell.prompt)
        if result.exit:
            self.root.destroy()


def run(config):
    root = tk.Tk()
    Terminal(root, config)
    root.mainloop()
