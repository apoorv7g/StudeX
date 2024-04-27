import tkinter as tk
from tkinter import messagebox

class TodoListApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List")

        self.tasks = []

        self.task_entry = tk.Entry(root, width=40)
        self.task_entry.grid(row=0, column=0, padx=10, pady=10)

        self.add_button = tk.Button(root, text="Add Task", command=self.add_task, bg="#4CAF50", fg="white")
        self.add_button.grid(row=0, column=1, padx=10, pady=10)

        self.task_list = tk.Listbox(root, width=50, height=10, borderwidth=0, highlightthickness=0)
        self.task_list.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        self.delete_button = tk.Button(root, text="Delete Task", command=self.delete_task, bg="#F44336", fg="white")
        self.delete_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="WE")

        self.task_list.bind("<<ListboxSelect>>", self.on_select)

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

    def on_select(self, event):
        try:
            index = self.task_list.curselection()[0]
            task = self.task_list.get(index)
            messagebox.showinfo("Task Selected", f"Selected Task: {task}")
        except IndexError:
            pass

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoListApp(root)
    root.mainloop()
