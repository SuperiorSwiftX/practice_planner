import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from .parser import parse_file
from .session import PracticeSessionController
from .timer import TimerWindow


class PracticePlanner(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Practice Planner")
        self.geometry("600x400")
        self.sections = {}
        self.entries = {}

        menubar = tk.Menu(self)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Open...", command=self.open_file)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        self.config(menu=menubar)

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True)

        self.btn = ttk.Button(self, text="Generate Plan", command=self.generate_plan)
        self.btn.pack(pady=10)

    def open_file(self):
        file_path = filedialog.askopenfilename(
            title="Select practise.txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
        )
        if not file_path:
            return
        self.sections = parse_file(file_path)
        self.populate_sections()

    def populate_sections(self):
        for tab in self.notebook.tabs():
            self.notebook.forget(tab)
        self.entries.clear()

        for section, exercises in self.sections.items():
            frame = ttk.Frame(self.notebook)
            self.notebook.add(frame, text=section)

            for ex in exercises:
                row = ttk.Frame(frame)
                row.pack(fill="x", pady=5)

                chk_var = tk.BooleanVar(value=False)
                chk = ttk.Checkbutton(row, text=ex, variable=chk_var)
                chk.pack(side="left", padx=5)

                time_label = ttk.Label(row, text="Minutes:")
                time_label.pack(side="left", padx=5)

                time_entry = ttk.Entry(row, width=5)
                time_entry.pack(side="left")

                self.entries[(section, ex)] = (chk_var, time_entry)

    def generate_plan(self):
        plan = []
        for (section, ex), (chk_var, time_entry) in self.entries.items():
            if chk_var.get():
                time_val = time_entry.get().strip()
                if not time_val.isdigit():
                    time_val = "0"
                minutes = int(time_val)
                if minutes > 0:
                    plan.append((section, ex, minutes))

        if plan:
            controller = PracticeSessionController(plan)
            TimerWindow(controller)
        else:
            messagebox.showwarning("Practice Plan", "No exercises selected!")
