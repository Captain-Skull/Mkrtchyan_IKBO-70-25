"""Окно терминала; команды исполняет независимый объект Shell."""

import tkinter as tk
from tkinter.scrolledtext import ScrolledText

from shell import Shell


class Terminal:
    def __init__(self, root: tk.Tk, vfs_name: str = "VFS"):
        self.root = root
        self.shell = Shell()
        root.title(f"Эмулятор оболочки — {vfs_name}")
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
        self.entry.focus_set()

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


def run():
    root = tk.Tk()
    Terminal(root)
    root.mainloop()
