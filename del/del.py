import tkinter as tk
from tkinter import messagebox, ttk


class TodoListApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List")
        self.root.configure(bg="#222222")

        # Styling
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TFrame", background="#222222")
        self.style.configure("TLabel", background="#222222", foreground="white")
        self.style.map("TButton", background=[("active", "#444444")])

        # Tasks
        self.tasks = []

        # Task Entry
        self.task_entry = ttk.Entry(root, width=40, font=("Arial", 12))
        self.task_entry.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.style.configure("TEntry", borderwidth=5, relief="solid", padding=5)

        # Add Task Button
        self.add_button = ttk.Button(root, text="Add Task", command=self.add_task)
        self.add_button.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        # Task List Frame
        self.task_list_frame = ttk.Frame(root)
        self.task_list_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        # Task List
        self.task_list = tk.Listbox(self.task_list_frame, width=50, height=10, font=("Arial", 12), bg="#333333",
                                    fg="white", bd=0, highlightthickness=0)
        self.task_list.pack(side="left", fill="both", expand=True)
        self.style.configure("TListbox", borderwidth=0, relief="solid", highlightthickness=0)

        # Scrollbar
        self.scrollbar = ttk.Scrollbar(self.task_list_frame, orient="vertical", command=self.task_list.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.task_list.config(yscrollcommand=self.scrollbar.set)

        # Bind events
        self.task_list.bind("<Button-1>", self.complete_task)

    def add_task(self):
        task = self.task_entry.get()
        if task:
            self.tasks.append(task)
            self.task_list.insert(tk.END, task)
            self.task_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Warning", "Please enter a task.")

    def complete_task(self, event):
        selection = self.task_list.curselection()
        if selection:
            index = selection[0]
            item = self.task_list.get(index)
            self.task_list.itemconfig(index, foreground="gray")
            self.task_list.selection_clear(index)


if __name__ == "__main__":
    root = tk.Tk()
    root.configure(bg="#222222")
    app = TodoListApp(root)
    root.mainloop()
