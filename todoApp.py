# Hello! I'm excited to share my second task, ToDo App. 🎉

# Here's the code: lets breakdown the code


# Import the json module to handle reading and writing JSON files
import json
# Import the tkinter module, which provides tools for creating graphical user interfaces (GUIs)
import tkinter as tk
# Import specific components from tkinter for additional functionality
from tkinter import messagebox, ttk, simpledialog, filedialog
# Import the Style class from the ttkbootstrap module to apply a Bootstrap theme to the GUI
from ttkbootstrap import Style


class TodoListApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Todo List App")
        self.geometry("530x400")

        # Set the style for the GUI components
        style = Style(theme="darkly")
        style.configure("Custom.TEntry", foreground="#555", borderwidth=30, bordercolor="#ccc", relief="solid", padding=(5, 10))

        # Create the input frame
        input_frame = ttk.Frame(self)
        input_frame.pack(pady=10)

        # Create and configure the task input entry
        self.task_input = ttk.Entry(input_frame, font="TkDefaultFont", width=70, style="Custom.TEntry")
        self.task_input.pack(side=tk.LEFT, padx=(15, 5), pady=10)
        self.task_input.insert(0, "Add your tasks here...")
        self.task_input.configure(foreground="white")
        self.task_input.bind("<FocusIn>", self.clear_placeholder)
        self.task_input.bind("<FocusOut>", self.restore_placeholder)

        # Create the "Add" button
        ttk.Button(input_frame, text="Add", command=self.add_task).pack(side=tk.LEFT, padx=(5, 10), pady=10)

        # Create and configure the task list
        self.task_list = tk.Listbox(self, font=("Poppins", 12), width=30, height=10, selectmode=tk.NONE)
        self.task_list.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        # Create buttons for different actions
        ttk.Button(self, text="Delete", style="danger.TButton", command=self.delete_task).pack(side=tk.RIGHT, padx=5, pady=10)
        ttk.Button(self, text="Done", style="Success.TButton", command=self.mark_done).pack(side=tk.RIGHT, padx=10, pady=10)
        ttk.Button(self, text="Load Task", command=self.load_tasks_from_file, style="danger.TButton").pack(side=tk.LEFT, padx=10, pady=10)
        ttk.Button(self, text="Save", command=self.save_tasks, style="Success.TButton").pack(side=tk.LEFT, padx=2, pady=10)
        ttk.Button(self, text="View Stats", style="info.TButton", command=self.view_stats).pack(side=tk.LEFT, padx=4, pady=10)
        ttk.Button(self, text="Edit Task", command=self.edit_task).pack(side=tk.LEFT, padx=4, pady=10)

        # Load existing tasks on application startup
        self.load_tasks()

    def add_task(self):
        # Get the task from the input field
        task = self.task_input.get()
        if task != "Add your tasks here...":
            # Generate task number and format the task text
            task_number = self.task_list.size() + 1

            task_text = f"Task {task_number}: {task}"
            # Insert the task into the listbox and configure its color
            self.task_list.insert(tk.END, task_text)
            self.task_list.itemconfig(tk.END, fg="#FABA5F")

            # Clear the input field and save tasks to the file
            self.task_input.delete(0, tk.END)
            self.save_tasks()

    def mark_done(self):
        # Get the index of the selected task
        task_index = self.task_list.curselection()
        if task_index:
            # Mark the selected task as done by changing its color to green
            self.task_list.itemconfig(task_index, fg="green")
            # Save the tasks to the file
            self.save_tasks()

    def delete_task(self):
        # Get the indices of the selected tasks
        selected_indices = self.task_list.curselection()
        if selected_indices:
            # Load existing tasks from the file or initialize an empty list
            try:
                with open("tasks.json", "r") as f:
                    data = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                data = []

            # Initialize a list to store deleted tasks
            deleted_tasks = []

            # Iterate through selected indices in reverse order to avoid index shifting
            for index in reversed(selected_indices):
                # Add the task to the deleted tasks list and remove it from the listbox
                deleted_tasks.append(self.task_list.get(index))
                self.task_list.delete(index)

            # Remove deleted tasks from the loaded data
            data = [task for task in data if task["text"] not in deleted_tasks]

            # Save the updated data back to the file
            with open("tasks.json", "w") as f:
                json.dump(data, f)

    def edit_task(self):
        # Get the index of the selected task
        selected_index = self.task_list.curselection()
        if selected_index:
            # Get the current text of the selected task
            current_text = self.task_list.get(selected_index)
            # Prompt the user to edit the task
            edited_text = simpledialog.askstring("Edit Task", "Edit your task:", initialvalue=current_text)

            if edited_text:
                # Remove the selected task and insert the edited task
                self.task_list.delete(selected_index)
                self.task_list.insert(selected_index, edited_text)
                self.task_list.itemconfig(selected_index, fg="orange")
                # Save the tasks to the file
                self.save_tasks()

    def view_stats(self):
        # Count the number of completed and total tasks
        done_count = 0
        total_count = self.task_list.size()
        for i in range(total_count):
            if self.task_list.itemcget(i, "fg") == "green":
                done_count += 1
        # Show a messagebox with task statistics
        messagebox.showinfo("Task Statistics", f"Total tasks: {total_count}\nCompleted tasks: {done_count}")

    def clear_placeholder(self, event):
        # Clear the placeholder text when the input field is focused
        if self.task_input.get() == "Add your tasks here...":
            self.task_input.delete(0, tk.END)
            self.task_input.configure(style="TEntry")

    def restore_placeholder(self, event):
        # Restore the placeholder text if the input field is empty
        if self.task_input.get() == "":
            self.task_input.insert(0, "Add your tasks here...")
            self.task_input.configure(style="Custom.TEntry")

    def load_tasks(self):
        try:
            # Load tasks from the file and populate the listbox with task data
            with open("tasks.json", "r") as f:
                data = json.load(f)
                if isinstance(data, list):
                    self.task_list.delete(0, tk.END)
                    for task in data:
                        if isinstance(task, dict) and "text" in task and "color" in task:
                            self.task_list.insert(tk.END, task["text"])
                            self.task_list.itemconfig(tk.END, fg=task["color"])
        except (FileNotFoundError, json.JSONDecodeError):
            pass

    def save_tasks(self):
        selected_indices = self.task_list.curselection()

        # Check if any task is selected
        if selected_indices:
            data = []
            if len(selected_indices) == self.task_list.size():
                # All tasks are selected, save all tasks
                for i in range(self.task_list.size()):
                    text = self.task_list.get(i)
                    color = self.task_list.itemcget(i, "fg")
                    data.append({"text": text, "color": color})
            else:
                # Only selected tasks are considered, save selected tasks
                for index in selected_indices:
                    text = self.task_list.get(index)
                    color = self.task_list.itemcget(index, "fg")
                    data.append({"text": text, "color": color})

            # Save the tasks to the file
            with open("tasks.json", "w") as f:
                json.dump(data, f)
            # Show a messagebox indicating successful task saving
            messagebox.showinfo("Tasks Saved", "Tasks saved successfully!")

    def load_tasks_from_file(self):
        # Open a file dialog to select a JSON file for loading tasks
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            try:
                # Load tasks from the selected file and populate the listbox with task data
                with open(file_path, "r") as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        self.task_list.delete(0, tk.END)
                        for task in data:
                            if isinstance(task, dict) and "text" in task and "color" in task:
                                self.task_list.insert(tk.END, task["text"])
                                self.task_list.itemconfig(tk.END, fg=task["color"])
                        # Show a messagebox indicating successful task loading
                        messagebox.showinfo("Tasks Loaded", "Tasks loaded successfully from the selected file.")
            except (FileNotFoundError, json.JSONDecodeError):
                # Show an error messagebox if there's an issue loading tasks from the file
                messagebox.showerror("Error", "Error loading tasks from the selected file.")


if __name__ == "__main__":
    # Create an instance of the TodoListApp and run the main loop
    app = TodoListApp()
    app.mainloop()

# Happy coding!
# Bye-bye!
# See you on my next task.!🚀😊