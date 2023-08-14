import os
import sys
import tkinter as tk
from tkinter import scrolledtext
from tkinter import ttk
from modules import *

class TextRedirector:
    def __init__(self, text_widget, tag="stdout"):
        self.text_widget = text_widget
        self.tag = tag

    def write(self, str):
        self.text_widget.configure(state=tk.NORMAL)
        self.text_widget.insert("end", str, (self.tag,))
        self.text_widget.configure(state=tk.DISABLED)
        self.text_widget.update_idletasks()

    def flush(self):
        pass

class MaintenanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Linux Maintenance App")

        self.setup_ui()

    def setup_ui(self):
        self.readme_text = scrolledtext.ScrolledText(self.root, width=80, height=10)
        self.readme_text.pack()

        self.display_readme()
        self.generate_module_buttons()

        exit_button = ttk.Button(self.root, text="Exit", command=self.exit_app)
        exit_button.pack()

    def display_readme(self):
        with open("README.md", "r") as readme_file:
            readme_content = readme_file.read()
            self.readme_text.insert(tk.END, readme_content)

    def generate_module_buttons(self):
        import importlib.util

        module_folders = ["modules", "additional_modules"]
        module_scripts = []

        for folder in module_folders:
            for module_file in os.listdir(folder):
                if module_file.endswith(".py") and module_file != "__init__.py":
                    module_name = os.path.splitext(module_file)[0]
                    module_path = os.path.join(folder, module_file)
                    full_module_name = f"{folder}.{module_name}"

                    spec = importlib.util.spec_from_file_location(full_module_name, module_path)
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    module_scripts.append(module)

        for script in module_scripts:
            module_name = script.__name__.split(".")[-1]
            label = " ".join(word.capitalize() for word in module_name.split("_"))

            button = ttk.Button(self.root, text=label, command=lambda s=script: self.execute_module(s))
            button.pack(side=tk.LEFT, padx=10, pady=10)

    def execute_module(self, module_script):
        self.readme_text.delete(1.0, tk.END)

        original_stdout = sys.stdout
        sys.stdout = TextRedirector(self.readme_text, "stdout")

        try:
            module_script()
        except Exception as e:
            print(f"An error occurred: {e}")

        sys.stdout = original_stdout

    def exit_app(self):
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = MaintenanceApp(root)
    root.mainloop()

