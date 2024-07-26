import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import DateEntry
from PIL import Image, ImageTk, ImageDraw
import random

class TodoApp:
    def __init__(self, root, image_path):
        self.root = root
        self.image_path = image_path
        self.root.title("To-Do List with Gradient Background")
        self.root.geometry("1000x800")
        self.root.resizable(True, True)

        self.tasks = {'personal': {}, 'professional': {}}
        self.task_var = tk.StringVar()
        self.current_date = tk.StringVar(value="")
        self.task_type = tk.StringVar(value="personal")
        self.selected_task = None

        # Set up the canvas for background image
        self.canvas = tk.Canvas(self.root)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Add the title
        self.title_label = tk.Label(self.canvas, text="To-Do List", font=('Helvetica', 24, 'bold'), bg='white', fg='black')
        self.title_label.pack(pady=20)

        # Update background image when the window is resized
        self.root.bind("<Configure>", self.update_background_image)

        # Create gradient overlay
        self.add_gradient_overlay()

        # Set up the sidebar frame with dropdown and calendar
        self.sidebar_frame = tk.Frame(self.canvas, bg='white', bd=5)
        self.sidebar_frame.place(relx=0.05, rely=0.05, anchor=tk.NW)

        self.date_entry = DateEntry(self.sidebar_frame, textvariable=self.current_date, date_pattern='yyyy-mm-dd', background='dark blue', foreground='white', borderwidth=2)
        self.date_entry.pack(pady=5)

        self.select_date_button = tk.Button(self.sidebar_frame, text="Select Date", command=self.select_date, bg='white', fg='black')
        self.select_date_button.pack(pady=5)

        self.type_label = tk.Label(self.sidebar_frame, text="Select Task Type", bg='white', fg='black')
        self.type_label.pack(pady=5)

        self.type_dropdown = ttk.Combobox(self.sidebar_frame, textvariable=self.task_type, values=["personal", "professional"], state="readonly")
        self.type_dropdown.pack(pady=5)
        self.type_dropdown.current(0)

        # Set up the to-do list section
        self.center_frame = tk.Frame(self.canvas, bd=5)
        self.center_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Create a Canvas for gradient background
        self.gradient_bg_canvas = tk.Canvas(self.center_frame, width=500, height=300, bd=0, highlightthickness=0)
        self.gradient_bg_canvas.grid(row=0, column=0, columnspan=2, padx=5, pady=5)
        self.apply_purple_gradient_background()

        # Create the Text widget
        self.task_text = tk.Text(self.center_frame, width=50, height=10, font=('Helvetica', 12), bg='light blue', fg='black', wrap=tk.WORD, state=tk.DISABLED)
        self.task_text.bind("<Button-1>", self.select_task)
        self.gradient_bg_canvas.create_window((0, 50), window=self.task_text, anchor='nw')

        self.task_entry = tk.Entry(self.center_frame, textvariable=self.task_var, width=40, font=('Helvetica', 12))
        self.gradient_bg_canvas.create_window((10, 10), window=self.task_entry, anchor='nw')

        self.add_task_button = tk.Button(self.center_frame, text="Add Task", command=self.add_task, bg='white', fg='black')
        self.gradient_bg_canvas.create_window((420, 10), window=self.add_task_button, anchor='nw')

        self.delete_task_button = tk.Button(self.center_frame, text="Delete Task", command=self.delete_task, bg='white', fg='black', state=tk.DISABLED)
        self.gradient_bg_canvas.create_window((220, 260), window=self.delete_task_button, anchor='nw')

        self.complete_task_button = tk.Button(self.center_frame, text="Complete Task", command=self.complete_task, bg='white', fg='black', state=tk.DISABLED)
        self.gradient_bg_canvas.create_window((10, 260), window=self.complete_task_button, anchor='nw')

        self.edit_task_button = tk.Button(self.center_frame, text="Edit Task", command=self.edit_task, bg='white', fg='black', state=tk.DISABLED)
        self.gradient_bg_canvas.create_window((110, 260), window=self.edit_task_button, anchor='nw')

        # Initialize tags
        self.task_text.tag_configure("completed", overstrike=True)
        self.task_text.tag_configure("task", foreground="black")
        self.task_text.tag_configure("selected", background="light gray")

        # Event binding for dynamic gradient change
        self.canvas.bind("<Enter>", self.change_gradient_on_hover)
        self.canvas.bind("<Leave>", self.reset_gradient)

        # Initialize date to today's date
        self.current_date.set(self.date_entry.get_date())
        self.update_task_list()

    def update_background_image(self, event=None):
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        try:
            img = Image.open(self.image_path)
            img_resized = img.resize((canvas_width, canvas_height), Image.LANCZOS)
            self.background_image = ImageTk.PhotoImage(img_resized)

            self.canvas.delete("background_image")  # Remove old background image
            self.canvas.create_image(0, 0, image=self.background_image, anchor='nw', tags="background_image")
        except Exception as e:
            print(f"Error loading image {self.image_path}: {e}")

    def add_gradient_overlay(self, start_color=(50, 50, 100), end_color=(0, 0, 50)):
        width, height = self.canvas.winfo_width(), self.canvas.winfo_height()
        gradient = Image.new('RGBA', (width, height), color=(0, 0, 0, 0))
        draw = ImageDraw.Draw(gradient)

        # Create a vertical gradient
        for i in range(height):
            r = int(start_color[0] + (end_color[0] - start_color[0]) * (i / height))
            g = int(start_color[1] + (end_color[1] - start_color[1]) * (i / height))
            b = int(start_color[2] + (end_color[2] - start_color[2]) * (i / height))
            draw.line((0, i, width, i), fill=(r, g, b, 128))

        self.gradient_image = ImageTk.PhotoImage(gradient)
        self.canvas.create_image(0, 0, image=self.gradient_image, anchor='nw', tags="gradient_overlay")
        self.canvas.tag_lower(self.gradient_image)  # Ensure gradient is behind other canvas items

    def change_gradient_on_hover(self, event=None):
        # Randomize colors for gradient
        start_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        end_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.add_gradient_overlay(start_color=start_color, end_color=end_color)

    def reset_gradient(self, event=None):
        # Reset to default gradient
        self.add_gradient_overlay()

    def select_date(self, event=None):
        # Update current date and refresh task list
        self.current_date.set(self.date_entry.get_date())
        self.update_task_list()

    def update_task_list(self):
        self.task_text.config(state=tk.NORMAL)  # Enable text widget to update
        self.task_text.delete(1.0, tk.END)
        self.task_text.tag_remove("task", 1.0, tk.END)
        self.task_text.tag_remove("completed", 1.0, tk.END)
        self.task_text.tag_remove("selected", 1.0, tk.END)

        date = self.current_date.get()
        task_type = self.task_type.get()
        if date in self.tasks[task_type]:
            for task, completed in self.tasks[task_type][date].items():
                tag = "completed" if completed else "task"
                self.task_text.insert(tk.END, f"{task}\n", tag)

        self.task_text.config(state=tk.DISABLED)  # Disable editing
        self.disable_buttons()

    def add_task(self):
        task = self.task_var.get()
        date = self.current_date.get()
        task_type = self.task_type.get()
        if task and date:
            if date not in self.tasks[task_type]:
                self.tasks[task_type][date] = {}
            self.tasks[task_type][date][task] = False
            self.task_var.set("")
            self.update_task_list()
        else:
            messagebox.showwarning("Input Error", "Please enter a task and select a date.")

    def delete_task(self):
        if self.selected_task:
            task = self.selected_task
            date = self.current_date.get()
            task_type = self.task_type.get()
            if date in self.tasks[task_type] and task in self.tasks[task_type][date]:
                del self.tasks[task_type][date][task]
                if not self.tasks[task_type][date]:
                    del self.tasks[task_type][date]
                self.selected_task = None
                self.update_task_list()
                self.disable_buttons()
        else:
            messagebox.showwarning("Selection Error", "No task selected for deletion.")

    def complete_task(self):
        if self.selected_task:
            task = self.selected_task
            date = self.current_date.get()
            task_type = self.task_type.get()
            if date in self.tasks[task_type] and task in self.tasks[task_type][date]:
                self.tasks[task_type][date][task] = True
                self.selected_task = None
                self.update_task_list()
                self.disable_buttons()
        else:
            messagebox.showwarning("Selection Error", "No task selected to mark as completed.")

    def edit_task(self):
        if self.selected_task:
            new_task = self.task_var.get()
            if new_task:
                date = self.current_date.get()
                task_type = self.task_type.get()
                if date in self.tasks[task_type] and self.selected_task in self.tasks[task_type][date]:
                    self.tasks[task_type][date][new_task] = self.tasks[task_type][date].pop(self.selected_task)
                    self.selected_task = new_task
                    self.task_var.set("")
                    self.update_task_list()
                    self.disable_buttons()
            else:
                messagebox.showwarning("Input Error", "Task description cannot be empty.")
        else:
            messagebox.showwarning("Selection Error", "No task selected for editing.")

    def select_task(self, event):
        index = self.task_text.index("@%s,%s" % (event.x, event.y))
        tag = self.task_text.tag_names(index)
        if "task" in tag:
            self.selected_task = self.task_text.get(index, "%s lineend" % index).strip()
            self.task_text.tag_add("selected", index, "%s lineend" % index)
            self.task_text.config(state=tk.DISABLED)
            self.enable_buttons()
        else:
            self.selected_task = None
            self.task_text.tag_remove("selected", 1.0, tk.END)
            self.disable_buttons()

    def enable_buttons(self):
        self.delete_task_button.config(state=tk.NORMAL)
        self.complete_task_button.config(state=tk.NORMAL)
        self.edit_task_button.config(state=tk.NORMAL)

    def disable_buttons(self):
        self.delete_task_button.config(state=tk.DISABLED)
        self.complete_task_button.config(state=tk.DISABLED)
        self.edit_task_button.config(state=tk.DISABLED)

    def apply_purple_gradient_background(self):
        width, height = 500, 300
        gradient = Image.new('RGBA', (width, height), color=(0, 0, 0, 0))
        draw = ImageDraw.Draw(gradient)
        for i in range(height):
            r = int(100 + (150 - 100) * (i / height))
            g = int(0 + (50 - 0) * (i / height))
            b = int(150 + (200 - 150) * (i / height))
            draw.line((0, i, width, i), fill=(r, g, b, 128))
        self.gradient_image = ImageTk.PhotoImage(gradient)
        self.gradient_bg_canvas.create_image(0, 0, image=self.gradient_image, anchor='nw')

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root, r"c:\Users\sivas\OneDrive\Pictures\bg-pat.jpg")  # Provide the correct path to your background image
    root.mainloop()
