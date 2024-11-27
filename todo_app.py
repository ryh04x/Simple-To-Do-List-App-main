import tkinter as tk
from tkinter import messagebox
import datetime
import os

class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Enhanced To-Do List")
        self.root.geometry("500x500")
        self.root.configure(bg="#2C2F38")

        # Display current date and time
        self.date_time_label = tk.Label(self.root, text="", font=("Helvetica", 12, "bold"), bg="#2C2F38", fg="#FFFFFF")
        self.date_time_label.pack(pady=10)
        self.update_time()

        # Title Label
        self.title_label = tk.Label(self.root, text="My To-Do List", font=("Helvetica", 16, "bold"), bg="#2C2F38", fg="#00FF7F")
        self.title_label.pack(pady=5)

        # Entry box for adding new tasks
        self.task_entry = tk.Entry(self.root, width=40, font=("Helvetica", 12), bg="#3B3F45", fg="#FFFFFF")
        self.task_entry.pack(pady=10)

        # Add Task Button
        self.add_button = tk.Button(self.root, text="Add Task", command=self.add_task, font=("Helvetica", 12, "bold"), 
                                     bg="#4CAF50", fg="black", cursor="hand2",
                                     activebackground="#45a049", activeforeground="black")
        self.add_button.pack(pady=5)

        # Listbox to display tasks
        self.task_listbox = tk.Listbox(self.root, width=40, height=10, font=("Helvetica", 12), selectmode=tk.SINGLE, 
                                       bg="#3B3F45", fg="#FFFFFF", activestyle="none")
        self.task_listbox.pack(pady=10)
        self.task_listbox.bind("<Double-Button-1>", self.toggle_task_completion)

        # Buttons for managing tasks
        self.delete_button = tk.Button(self.root, text="Delete Task", command=self.delete_task, font=("Helvetica", 12, "bold"), 
                                       bg="#FF4B5C", fg="black", cursor="hand2", 
                                       activebackground="#ff6659", activeforeground="black")
        self.delete_button.pack(pady=5)

        self.clear_button = tk.Button(self.root, text="Clear All Tasks", command=self.clear_tasks, font=("Helvetica", 12, "bold"), 
                                      bg="#1E5128", fg="black", cursor="hand2", 
                                      activebackground="#2d6b42", activeforeground="black")
        self.clear_button.pack(pady=5)

        # Remaining tasks label
        self.task_count_label = tk.Label(self.root, text="Tasks Remaining: 0", font=("Helvetica", 12, "italic"), 
                                         bg="#2C2F38", fg="#FFFFFF")
        self.task_count_label.pack(pady=10)

        # Load tasks from file
        self.load_tasks()

    def update_time(self):
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.date_time_label.config(text=current_time)
        self.root.after(1000, self.update_time)

    def add_task(self):
        task = self.task_entry.get().strip()
        if task:
            self.task_listbox.insert(tk.END, task)
            self.task_entry.delete(0, tk.END)
            self.update_task_count()
        else:
            messagebox.showwarning("Input Error", "Please enter a task.")

    def delete_task(self):
        try:
            selected_task_index = self.task_listbox.curselection()[0]
            self.task_listbox.delete(selected_task_index)
            self.update_task_count()
        except IndexError:
            messagebox.showwarning("Selection Error", "Please select a task to delete.")

    def clear_tasks(self):
        if messagebox.askyesno("Clear All", "Are you sure you want to clear all tasks?"):
            self.task_listbox.delete(0, tk.END)
            self.update_task_count()

    def toggle_task_completion(self, event):
        selected_index = self.task_listbox.curselection()
        if selected_index:
            index = selected_index[0]
            task_text = self.task_listbox.get(index)
            if task_text.startswith("✔ "):
                self.task_listbox.delete(index)
                self.task_listbox.insert(index, task_text[2:])
                self.task_listbox.itemconfig(index, {'fg': '#FFFFFF'})
            else:
                self.task_listbox.delete(index)
                self.task_listbox.insert(index, "✔ " + task_text)
                self.task_listbox.itemconfig(index, {'fg': '#888888'})
            self.update_task_count()

    def update_task_count(self):
        total_tasks = self.task_listbox.size()
        completed_tasks = len([self.task_listbox.get(i) for i in range(total_tasks) if self.task_listbox.get(i).startswith("✔ ")])
        remaining_tasks = total_tasks - completed_tasks
        self.task_count_label.config(text=f"Tasks Remaining: {remaining_tasks}")

    def save_tasks(self):
        with open("tasks.txt", "w") as file:
            for i in range(self.task_listbox.size()):
                file.write(self.task_listbox.get(i) + "\n")

    def load_tasks(self):
        if os.path.exists("tasks.txt"):
            with open("tasks.txt", "r") as file:
                tasks = file.readlines()
                for task in tasks:
                    self.task_listbox.insert(tk.END, task.strip())
                    if task.startswith("✔ "):
                        index = self.task_listbox.size() - 1
                        self.task_listbox.itemconfig(index, {'fg': '#888888'})
            self.update_task_count()

    def on_close(self):
        self.save_tasks()
        self.root.destroy()

# Set up the main application window
def run_todo_app():
    root = tk.Tk()
    app = ToDoApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()

# Run the application
if __name__ == "__main__":
    run_todo_app()
