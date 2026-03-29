import os
import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List")

        self.tasks = self.load_tasks()

        self.task_listbox = tk.Listbox(root, selectmode=tk.SINGLE)
        self.task_listbox.pack(pady=10)

        self.update_task_listbox()

        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)

        view_button = tk.Button(button_frame, text="View", command=self.view_task)
        add_button = tk.Button(button_frame, text="Add", command=self.add_task)
        update_button = tk.Button(button_frame, text="Update", command=self.update_task)
        mark_completed_button = tk.Button(button_frame, text="Mark Completed", command=self.mark_completed)
        delete_button = tk.Button(button_frame, text="Delete", command=self.delete_task)

        view_button.grid(row=0, column=0, padx=5)
        add_button.grid(row=0, column=1, padx=5)
        update_button.grid(row=0, column=2, padx=5)
        mark_completed_button.grid(row=0, column=3, padx=5)
        delete_button.grid(row=0, column=4, padx=5)

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def load_tasks(self):
        tasks = []
        filename = "todo_list.txt"
        if os.path.exists(filename):
            with open(filename, "r") as file:
                tasks = [line.strip() for line in file]
        return tasks

    def save_tasks(self):
        filename = "todo_list.txt"
        with open(filename, "w") as file:
            for task in self.tasks:
                file.write(task + "\n")

    def update_task_listbox(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            self.task_listbox.insert(tk.END, task)

    def view_task(self):
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            messagebox.showinfo("Task Details", self.tasks[selected_task_index[0]])
        else:
            messagebox.showinfo("Error", "Please select a task to view.")

    def add_task(self):
        task = simpledialog.askstring("Add Task", "Enter the new task:")
        if task:
            self.tasks.append(task)
            self.update_task_listbox()

    def update_task(self):
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            new_task = simpledialog.askstring("Update Task", "Enter the new task:")
            if new_task:
                self.tasks[selected_task_index[0]] = new_task
                self.update_task_listbox()
        else:
            messagebox.showinfo("Error", "Please select a task to update.")

    def mark_completed(self):
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            completed_task = self.tasks.pop(selected_task_index[0])
            messagebox.showinfo("Task Completed", f"Task '{completed_task}' marked as completed.")
            self.update_task_listbox()
        else:
            messagebox.showinfo("Error", "Please select a task to mark as completed.")

    def delete_task(self):
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            deleted_task = self.tasks.pop(selected_task_index[0])
            messagebox.showinfo("Task Deleted", f"Task '{deleted_task}' deleted successfully.")
            self.update_task_listbox()
        else:
            messagebox.showinfo("Error", "Please select a task to delete.")

    def on_close(self):
        self.save_tasks()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()
