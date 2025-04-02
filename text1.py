import tkinter as tk
from tkinter import ttk, filedialog, simpledialog, font

class TextEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Text Editor")

        # Styling
        self.style = ttk.Style()
        self.style.theme_use("clam")  # Choose a theme (aqua, clam, alt, default, etc.)

        # Text Widget
        self.text_widget = tk.Text(self.root, wrap="word", undo=True, font=("Helvetica", 12))
        self.text_widget.pack(expand="yes", fill="both")

        # Menu Bar
        self.menu_bar = tk.Menu(root)
        self.root.config(menu=self.menu_bar)

        # File Menu
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="New", command=self.new_file)
        self.file_menu.add_command(label="Open", command=self.open_file)
        self.file_menu.add_command(label="Save", command=self.save_file)
        self.file_menu.add_command(label="Save As", command=self.save_as_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.root.destroy)

        # Edit Menu
        self.edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)
        self.edit_menu.add_command(label="Undo", command=self.text_widget.edit_undo)
        self.edit_menu.add_command(label="Redo", command=self.text_widget.edit_redo)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Cut", command=self.cut)
        self.edit_menu.add_command(label="Copy", command=self.copy)
        self.edit_menu.add_command(label="Paste", command=self.paste)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Select All", command=self.select_all)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Find", command=self.find_text)
        self.edit_menu.add_command(label="Replace", command=self.replace_text)

        # Font Menu
        self.font_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Font", menu=self.font_menu)
        self.font_menu.add_command(label="Change Font", command=self.change_font)
        self.font_menu.add_command(label="Change Font Size", command=self.change_font_size)

        # View Menu
        self.view_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="View", menu=self.view_menu)
        self.view_menu.add_command(label="Toggle Status Bar", command=self.toggle_status_bar)

        # Status Bar
        self.status_var = tk.StringVar()
        self.status_bar = ttk.Label(root, textvariable=self.status_var, anchor=tk.W, relief=tk.SUNKEN)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # Default status
        self.status_var.set("Ready")

    def new_file(self):
        self.text_widget.delete("1.0", tk.END)
        self.root.title("Text Editor")
        self.update_status("New file created")

    def open_file(self):
        file_path = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, "r") as file:
                file_content = file.read()
                self.text_widget.delete("1.0", tk.END)
                self.text_widget.insert(tk.END, file_content)
            self.root.title(f"Text Editor - {file_path}")
            self.update_status(f"Opened file: {file_path}")

    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, "w") as file:
                file.write(self.text_widget.get("1.0", tk.END))
            self.root.title(f"Text Editor - {file_path}")
            self.update_status(f"Saved file: {file_path}")

    def save_as_file(self):
        self.save_file()

    def cut(self):
        self.text_widget.event_generate("<<Cut>>")
        self.update_status("Cut")

    def copy(self):
        self.text_widget.event_generate("<<Copy>>")
        self.update_status("Copy")

    def paste(self):
        self.text_widget.event_generate("<<Paste>>")
        self.update_status("Paste")

    def select_all(self):
        self.text_widget.tag_add(tk.SEL, "1.0", tk.END)
        self.text_widget.mark_set(tk.SEL_FIRST, "1.0")
        self.text_widget.mark_set(tk.SEL_LAST, tk.END)
        self.text_widget.see(tk.SEL_FIRST)
        self.update_status("Selected all")

    def find_text(self):
        query = simpledialog.askstring("Find", "Enter text to find:")
        if query:
            start_pos = "1.0"
            while True:
                start_pos = self.text_widget.search(query, start_pos, stopindex=tk.END)
                if not start_pos:
                    break
                end_pos = f"{start_pos}+{len(query)}c"
                self.text_widget.tag_add(tk.SEL, start_pos, end_pos)
                start_pos = end_pos
            self.text_widget.tag_configure("sel", background="yellow")
            self.update_status(f"Found occurrences of: {query}")

    def replace_text(self):
        find_query = simpledialog.askstring("Find", "Enter text to find:")
        if find_query:
            replace_query = simpledialog.askstring("Replace", f"Replace '{find_query}' with:")
            if replace_query:
                content = self.text_widget.get("1.0", tk.END)
                updated_content = content.replace(find_query, replace_query)
                self.text_widget.delete("1.0", tk.END)
                self.text_widget.insert(tk.END, updated_content)
                self.update_status(f"Replaced occurrences of: {find_query}")

    def change_font(self):
        font_name = simpledialog.askstring("Font", "Enter font (e.g., Arial, Times New Roman):")
        if font_name:
            current_font = font.Font(self.text_widget, self.text_widget.cget("font"))
            current_font.configure(family=font_name)
            self.text_widget.configure(font=current_font)
            self.update_status(f"Changed font to: {font_name}")

    def change_font_size(self):
        size = simpledialog.askinteger("Font Size", "Enter font size:")
        if size:
            current_font = font.Font(self.text_widget, self.text_widget.cget("font"))
            current_font.configure(size=size)
            self.text_widget.configure(font=current_font)
            self.update_status(f"Changed font size to: {size}")

    def toggle_status_bar(self):
        if self.status_bar.winfo_ismapped():
            self.status_bar.pack_forget()
            self.update_status("Status Bar hidden")
        else:
            self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
            self.update_status("Status Bar shown")

    def update_status(self, message):
        self.status_var.set(message)

if __name__ == "__main__":
    root = tk.Tk()
    app = TextEditor(root)
    root.mainloop()
