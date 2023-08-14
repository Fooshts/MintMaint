import os
import sys
import tkinter as tk
from tkinter import scrolledtext
from tkinter import ttk
import importlib.util
import modules.exit_module  # Import the exit_module from the modules package

# Define a class for redirecting text to a tkinter Text widget
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

# Define the main application class
class MaintenanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Linux Maintenance App")
        self.exit_module = importlib.import_module("modules.exit_module")  # Import the exit_module from the modules package
        self.setup_ui()

    def setup_ui(self):
        # Create a scrolled text area to display README.md content
        self.readme_text = scrolledtext.ScrolledText(self.root, width=80, height=10)
        self.readme_text.pack()

        # Display README.md content
        self.display_readme()

        # Generate and display buttons for modules
        self.generate_module_buttons()
        
    def display_readme(self):
        with open("README.md", "r") as readme_file:
            readme_content = readme_file.read()
            self.readme_text.insert(tk.END, readme_content)

    def generate_module_buttons(self):
        # Discover and import all module scripts from the modules and additional_modules folders
        module_folders = ["modules", "additional_modules"]
        module_scripts = []

        for folder in module_folders:
            for module_file in os.listdir(folder):
                if module_file.endswith(".py") and module_file != "__init__.py":
                    module_name = os.path.splitext(module_file)[0]
                    module_path = os.path.join(folder, module_file)

                    # Construct the full module name to be imported
                    full_module_name = f"{folder}.{module_name}"

                    # Use importlib to dynamically import the module
                    spec = importlib.util.spec_from_file_location(full_module_name, module_path)
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    module_scripts.append(module)

        # Add an "Exit" button using the exit module
        exit_button = ttk.Button(self.root, text="Exit", command=lambda: self.exit_module.exit_app(self.root))
        exit_button.pack(side=tk.RIGHT, padx=10, pady=10)



        # Generate buttons for the discovered module scripts using pack
        for script in module_scripts:
            module_name = script.__name__.split(".")[-1]
            label = " ".join(word.capitalize() for word in module_name.split("_"))

            if module_name == "exit_module":  # Skip the exit_module
                continue

            # Extract the specific function from the module and pass it to execute_module
            function_to_call = getattr(script, module_name)
            button = ttk.Button(self.root, text=label, command=lambda f=function_to_call: self.execute_module(f))
            button.pack(side=tk.LEFT, padx=10, pady=10)

    def execute_module(self, module_script):
        # Clear the output area
        self.readme_text.delete(1.0, tk.END)

        # Redirect the standard output to the scrolled text area
        original_stdout = sys.stdout
        sys.stdout = TextRedirector(self.readme_text, "stdout")

        # Execute the selected module script
        try:
            result = module_script()  # Call the function within the module
            print(result)  # Print the result to the redirected output
        except Exception as e:
            print(f"An error occurred: {e}")

        # Restore the original standard output
        sys.stdout = original_stdout

# Main entry point of the program
if __name__ == "__main__":
    root = tk.Tk()  # Create the main tkinter window
    app = MaintenanceApp(root)  # Create an instance of the MaintenanceApp class
    root.mainloop()  # Start the tkinter event loop
