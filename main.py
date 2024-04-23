import tkinter as tk
from tkinter import messagebox, filedialog
import os
import zipfile

class AutomateTheBoringStuffApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Automate The Boring Stuff")
        self.root.geometry("600x600")

        # Variables to store user inputs
        self.new_client_name = tk.StringVar()
        self.old_client_name = tk.StringVar()

        # Pages
        self.pages = []

        # Create form page
        self.create_form_page()

        # Initially show form page
        self.show_page(0)

        # Create menu
        self.create_menu()

    def create_menu(self):
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        nav_menu = tk.Menu(menu_bar, tearoff=0)
        nav_menu.add_command(label="Previous", command=self.show_previous_page)
        nav_menu.add_command(label="Next", command=self.show_next_page)

        menu_bar.add_cascade(label="Navigation", menu=nav_menu)

    def create_form_page(self):
        form_frame = tk.Frame(self.root)
        form_frame.place(relx=0.5, rely=0.5, anchor="center")
        self.pages.append(form_frame)

        # Labels and entry widgets for user input
        tk.Label(form_frame, text="New Client Business Name:").grid(row=0, column=0, sticky="w")
        self.new_client_entry = tk.Entry(form_frame, textvariable=self.new_client_name)
        self.new_client_entry.grid(row=0, column=1)

        tk.Label(form_frame, text="Old Client Business Name:").grid(row=1, column=0, sticky="w")
        self.old_client_entry = tk.Entry(form_frame, textvariable=self.old_client_name)
        self.old_client_entry.grid(row=1, column=1)

        # Submit button
        submit_btn = tk.Button(form_frame, text="Submit", command=self.submit_form)
        submit_btn.grid(row=2, columnspan=2, pady=10)

    def create_result_page(self, new_client, old_client):
        result_frame = tk.Frame(self.root)
        result_frame.place(relx=0.5, rely=0.5, anchor="center")
        self.pages.append(result_frame)

        # Display user inputs in a text widget
        output_text = f"New Client Business Name: {new_client}\nOld Client Business Name: {old_client}"
        output_text_widget = tk.Text(result_frame, height=5, width=50)
        output_text_widget.insert(tk.END, output_text)
        output_text_widget.pack()

        # Frame for buttons
        button_frame = tk.Frame(result_frame)
        button_frame.pack()

        # Buttons to save text file and open zip file
        save_btn = tk.Button(button_frame, text="Save Text File", command=lambda: self.save_text_file(output_text))
        save_btn.pack(side=tk.LEFT, padx=10)

        open_zip_btn = tk.Button(button_frame, text="Open Zip File", command=self.open_zip_file)
        open_zip_btn.pack(side=tk.LEFT, padx=10)

    def submit_form(self):
        # Get user inputs
        new_client = self.new_client_name.get()
        old_client = self.old_client_name.get()

        # Remove form page
        self.pages[0].destroy()

        # Create result page
        self.create_result_page(new_client, old_client)

    def show_page(self, index):
        self.pages[index].tkraise()

    def show_previous_page(self):
        current_index = self.pages.index(self.root.focus_get().winfo_parent())
        previous_index = current_index - 1 if current_index > 0 else len(self.pages) - 1
        self.show_page(previous_index)

    def show_next_page(self):
        current_index = self.pages.index(self.root.focus_get().winfo_parent())
        next_index = (current_index + 1) % len(self.pages)
        self.show_page(next_index)

    def save_text_file(self, text):
        filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if filename:
            with open(filename, "w") as file:
                file.write(text)
            messagebox.showinfo("Success", "Text file saved successfully!")

    def open_zip_file(self):
        zip_filename = filedialog.askopenfilename(filetypes=[("Zip files", "*.zip")])
        if zip_filename:
            with zipfile.ZipFile(zip_filename, "r") as zip_ref:
                zip_ref.extractall()
            messagebox.showinfo("Success", "Zip file extracted successfully!")


if __name__ == "__main__":
    root = tk.Tk()
    app = AutomateTheBoringStuffApp(root)
    root.mainloop()
