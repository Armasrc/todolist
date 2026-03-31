import os
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox

class FormatDialog(simpledialog.Dialog):
    def __init__(self, parent, title="Formato pasirinkimas"):
        self.choice = "Nėra"
        super().__init__(parent, title)

    def body(self, master):
        ttk.Label(master, text="Pasirinkite formatą:").grid(row=0, column=0, padx=10, pady=(10, 0), sticky="w")
        self.format_var = tk.StringVar(value="Nėra")
        options = ["Nėra", "Paryškintas", "Kursyvas", "Žymėti", "Perbraukti"]
        self.option_menu = ttk.OptionMenu(master, self.format_var, options[0], *options)
        self.option_menu.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        return self.option_menu

    def buttonbox(self):
        box = ttk.Frame(self)
        ok_button = ttk.Button(box, text="OK", width=10, command=self.ok, default="active")
        ok_button.pack(side=tk.LEFT, padx=5, pady=5)
        cancel_button = ttk.Button(box, text="Atšaukti", width=10, command=self.cancel)
        cancel_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)
        box.pack()

    def apply(self):
        self.choice = self.format_var.get()

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Užrašinė")
        self.root.geometry("500x450")
        self.root.minsize(450, 400)

        # Style configuration
        style = ttk.Style()
        style.theme_use("clam")
        
        # --- Dark theme colors ---
        dark_bg = "#1e1e1e"
        dark_fg = "#ffffff"
        accent = "#3a7ff6"

        # Window background
        self.root.configure(bg=dark_bg)

        # Global styles
        style.configure(".", background=dark_bg, foreground=dark_fg, fieldbackground=dark_bg)
        style.configure("Title.TLabel", background=dark_bg, foreground=dark_fg)
        style.configure("Accent.TButton", background=accent, foreground="white")
        style.map("Accent.TButton", background=[("active", "#2f6ad9")])
        style.configure("Title.TLabel", font=("Segoe UI", 18, "bold"))
        style.configure("Task.TLabel", font=("Segoe UI", 10))
        style.configure("Accent.TButton", font=("Segoe UI", 10, "bold"), padding=6)

        # Title label
        title_label = ttk.Label(root, text="Mano Užrašinė", style="Title.TLabel")
        title_label.pack(pady=(15, 10))

        # Main frame
        main_frame = ttk.Frame(root, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Listbox frame with scrollbar
        list_frame = ttk.Frame(main_frame)
        list_frame.pack(fill=tk.BOTH, expand=True)

        self.task_listbox = tk.Listbox(
            list_frame,
            font=("Segoe UI", 11),
            selectmode=tk.SINGLE,
            activestyle="none",
            height=12,
            bg="#1e1e1e",
            fg="#ffffff",
            selectbackground="#3a7ff6",
            selectforeground="white",
            relief=tk.FLAT,
            borderwidth=0
        )

        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.task_listbox.yview)
        self.task_listbox.config(yscrollcommand=scrollbar.set)

        self.task_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=10)

        buttons = [
            ("Peržiūrėti", self.view_task),
            ("Pridėti", self.add_task),
            ("Atnaujinti", self.update_task),
            ("Formatuoti", self.format_task),
            ("Žymėti", self.toggle_checkbox),
            ("Užbaigti", self.mark_completed),
            ("Ištrinti", self.delete_task),
        ]

        for i, (text, command) in enumerate(buttons):
            btn = ttk.Button(
                button_frame,
                text=text,
                command=command,
                style="Accent.TButton"
            )
            btn.grid(row=0, column=i, padx=5, pady=5, sticky="ew")

        for i in range(len(buttons)):
            button_frame.columnconfigure(i, weight=1)

        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Paruošta")
        status_bar = ttk.Label(root, textvariable=self.status_var, anchor="w", padding=5)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # Keyboard shortcuts
        self.root.bind("<Delete>", lambda e: self.delete_task())
        self.root.bind("<Return>", lambda e: self.view_task())
        self.root.bind("<Control-n>", lambda e: self.add_task())

        self.tasks = self.load_tasks()
        self.update_task_listbox()

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def load_tasks(self):
        tasks = []
        filename = "todo_list.txt"
        if os.path.exists(filename):
            with open(filename, "r", encoding="utf-8") as file:
                tasks = [line.strip() for line in file]
        return tasks

    def save_tasks(self):
        filename = "todo_list.txt"
        with open(filename, "w", encoding="utf-8") as file:
            for task in self.tasks:
                file.write(task + "\n")

    def choose_format(self):
        format_dialog = FormatDialog(self.root)
        return format_dialog.choice

    def apply_text_format(self, text, style):
        if style == "Paryškintas":
            return self.to_bold(text)
        if style == "Kursyvas":
            return self.to_italic(text)
        if style == "Žymėti":
            return self.toggle_checkbox_state(text)
        if style == "Perbraukti":
            return self.to_strikethrough(text)
        if style == "Nėra":
            return text
        return text

    def to_bold(self, text):
        bold_mapping = {}
        for i, char in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
            bold_mapping[char] = chr(0x1D400 + i)
        for i, char in enumerate("abcdefghijklmnopqrstuvwxyz"):
            bold_mapping[char] = chr(0x1D41A + i)
        for i, char in enumerate("0123456789"):
            bold_mapping[char] = chr(0x1D7CE + i)
        return "".join(bold_mapping.get(ch, ch) for ch in text)

    def to_italic(self, text):
        italic_mapping = {}
        for i, char in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
            italic_mapping[char] = chr(0x1D434 + i)
        for i, char in enumerate("abcdefghijklmnopqrstuvwxyz"):
            italic_mapping[char] = chr(0x1D44E + i)
        return "".join(italic_mapping.get(ch, ch) for ch in text)

    def to_strikethrough(self, text):
        return "".join((ch + "\u0336") if ch != " " else ch for ch in text)

    def toggle_checkbox_state(self, text):
        if text.startswith("☐ "):
            return "☑ " + text[2:]
        if text.startswith("☑ "):
            return "☐ " + text[2:]
        return "☐ " + text

    def update_task_listbox(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            self.task_listbox.insert(tk.END, task)
        self.status_var.set(f"Įrašų skaičius: {len(self.tasks)}")

    def get_selected_index(self):
        selection = self.task_listbox.curselection()
        if not selection:
            messagebox.showwarning("Nepažymėtas įrašas", "Prašome pasirinkti įrašą.")
            return None
        return selection[0]

    def view_task(self):
        index = self.get_selected_index()
        if index is not None:
            messagebox.showinfo("Įrašo info", self.tasks[index])
            self.status_var.set("Peržiūrėtas įrašas")

    def add_task(self):
        task = simpledialog.askstring("Pridėti įrašą", "Įrašykite norimą įrašą:")
        if task:
            format_choice = self.choose_format()
            task = self.apply_text_format(task, format_choice)
            self.tasks.append(task)
            self.update_task_listbox()
            self.status_var.set("Įrašas pridėtas")

    def update_task(self):
        index = self.get_selected_index()
        if index is not None:
            new_task = simpledialog.askstring("Atnaujinti įrašą", "Įrašykite norimą įrašą:")
            if new_task:
                format_choice = self.choose_format()
                self.tasks[index] = self.apply_text_format(new_task, format_choice)
                self.update_task_listbox()
                self.status_var.set("Įrašas atnaujintas")

    def format_task(self):
        index = self.get_selected_index()
        if index is not None:
            format_choice = self.choose_format()
            if format_choice and format_choice != "Nėra":
                self.tasks[index] = self.apply_text_format(self.tasks[index], format_choice)
                self.update_task_listbox()
                self.status_var.set(f"Įrašas suformatuotas: {format_choice}")
            else:
                self.status_var.set("Nėra formato pakeitimų")

    def toggle_checkbox(self):
        index = self.get_selected_index()
        if index is not None:
            current = self.tasks[index]
            updated = self.toggle_checkbox_state(current)
            self.tasks[index] = updated
            self.update_task_listbox()
            if updated.startswith("☑"):
                self.status_var.set("Žymeklis pažymėtas")
            else:
                self.status_var.set("Žymeklis atžymėtas")

    def mark_completed(self):
        index = self.get_selected_index()
        if index is not None:
            completed_task = self.tasks.pop(index)
            messagebox.showinfo("Užbaigta", f"Užduotis '{completed_task}' užbaigta.")
            self.update_task_listbox()
            self.status_var.set("Užduotis užbaigta")

    def delete_task(self):
        index = self.get_selected_index()
        if index is not None:
            confirm = messagebox.askyesno("Patvirtinimas", "Ar tikrai norite ištrinti šį įrašą?")
            if confirm:
                deleted_task = self.tasks.pop(index)
                self.update_task_listbox()
                self.status_var.set(f"Ištrinta: {deleted_task}")

    def on_close(self):
        self.save_tasks()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()

