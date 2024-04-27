import tkinter as tk
from tkinter import messagebox, ttk

class TodoListApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List")

        # Styling
        self.style = ttk.Style()
        self.style.theme_use("clam")

        self.tasks = []

        # Task Entry
        self.task_entry = ttk.Entry(root, width=40, font=("Arial", 12))
        self.task_entry.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        # Add Task Button
        self.add_button = ttk.Button(root, text="Add Task", command=self.add_task)
        self.add_button.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        # Task List
        self.task_list = tk.Listbox(root, width=50, height=10, font=("Arial", 12), bd=0, highlightthickness=0)
        self.task_list.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        # Scrollbar
        self.scrollbar = ttk.Scrollbar(root, orient="vertical", command=self.task_list.yview)
        self.scrollbar.grid(row=1, column=2, sticky="ns")
        self.task_list.config(yscrollcommand=self.scrollbar.set)

        # Delete Task Button
        self.delete_button = ttk.Button(root, text="Delete Task", command=self.delete_task)
        self.delete_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        # Set weights for resizing
        root.columnconfigure(0, weight=1)
        root.columnconfigure(1, weight=1)
        root.rowconfigure(1, weight=1)

    def add_task(self):
        task = self.task_entry.get()
        if task:
            self.tasks.append(task)
            self.task_list.insert(tk.END, task)
            self.task_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Warning", "Please enter a task.")

    def delete_task(self):
        try:
            index = self.task_list.curselection()[0]
            del self.tasks[index]
            self.task_list.delete(index)
        except IndexError:
            messagebox.showwarning("Warning", "Please select a task to delete.")

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoListApp(root)
    root.mainloop()
