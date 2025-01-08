import tkinter as tk
from tkinter import scrolledtext, ttk, font, filedialog, messagebox
from triebase import Trie
from fpdf import FPDF  # Importing the library for PDF creation


def run_text_edtior():
    class AutoFillText(scrolledtext.ScrolledText):
        def __init__(self, master, trie, stats_callback=None, **kwargs):
            super().__init__(master, **kwargs)
            self.trie = trie
            self.stats_callback = stats_callback
            self.suggestion_box = None
            self.bind("<KeyRelease>", self.on_key_release)

        def on_key_release(self, event):
            if event.keysym in ("Return", "Tab", "Shift_L", "Shift_R", "Control_L", "Control_R"):
                return

            # Update statistics
            if self.stats_callback:
                self.stats_callback()

            # Show suggestions
            self.show_suggestions()

        def show_suggestions(self):
            self.delete_suggestions()

            current_text = self.get("1.0", tk.END).strip()
            if not current_text:
                return

            words = current_text.split()
            last_word = words[-1] if words else ""
            suggestions = self.trie.starts_with(last_word)

            if suggestions:
                self.suggestion_box = tk.Toplevel(self)
                self.suggestion_box.overrideredirect(1)
                self.suggestion_box.geometry(f"+{self.winfo_rootx()}+{self.winfo_rooty() + self.winfo_height()}")
                suggestion_list = tk.Listbox(self.suggestion_box, bg="lightgrey", fg="black", font=("Arial", 12))
                suggestion_list.pack(side="left", fill="both", expand=True)
                scrollbar = tk.Scrollbar(self.suggestion_box, orient="vertical")
                scrollbar.pack(side="right", fill="y")
                suggestion_list.config(yscrollcommand=scrollbar.set)
                scrollbar.config(command=suggestion_list.yview)

                for suggestion in suggestions:
                    suggestion_list.insert(tk.END, suggestion)

                suggestion_list.bind("<<ListboxSelect>>", self.on_suggestion_select)

        def on_suggestion_select(self, event):
            if not self.suggestion_box:
                return

            suggestion_list = event.widget
            selected_index = suggestion_list.curselection()
            if selected_index:
                selected_text = suggestion_list.get(selected_index)
                current_text = self.get("1.0", tk.END).strip()
                words = current_text.split()
                words[-1] = selected_text
                self.delete("1.0", tk.END)
                self.insert("1.0", " ".join(words))
                self.suggestion_box.destroy()
                self.suggestion_box = None

        def delete_suggestions(self):
            if self.suggestion_box:
                self.suggestion_box.destroy()
                self.suggestion_box = None

    def update_statistics():
        content = auto_fill_text.get("1.0", tk.END).strip()

        # Calculate statistics
        word_count = len(content.split())
        character_count = len(content)
        reading_time = round(word_count / 200, 2)  # Assuming 200 WPM reading speed

        # Update the labels
        word_count_label.config(text=f"Words: {word_count}")
        char_count_label.config(text=f"Characters: {character_count}")
        reading_time_label.config(text=f"Reading Time: {reading_time} mins")

    def apply_tag(tag_name, **kwargs):
        selected_text = auto_fill_text.tag_ranges("sel")
        if not selected_text:
            return  # No selection made
        auto_fill_text.tag_add(tag_name, *selected_text)
        auto_fill_text.tag_config(tag_name, **kwargs)

    def toggle_bold():
        apply_tag("bold", font=font.Font(auto_fill_text, weight="bold"))

    def toggle_italic():
        apply_tag("italic", font=font.Font(auto_fill_text, slant="italic"))

    def change_font_family(family):
        current_font = font.Font(auto_fill_text)
        apply_tag("font_family", font=font.Font(auto_fill_text, family=family, size=current_font.cget("size")))

    def change_font_size(size):
        current_font = font.Font(auto_fill_text)
        apply_tag("font_size", font=font.Font(auto_fill_text, family=current_font.cget("family"), size=size))

    def export_as_pdf():
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf",
                                                 filetypes=[("PDF Files", "*.pdf")],
                                                 title="Save as PDF")
        if not file_path:
            return  # User canceled the save dialog

        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        # Retrieve content from the text widget
        content = auto_fill_text.get("1.0", tk.END).strip()

        for line in content.split("\n"):
            pdf.cell(0, 10, txt=line, ln=True, align="L")

        try:
            pdf.output(file_path)
            messagebox.showinfo("Export Successful", f"Document has been exported to {file_path}")
        except Exception as e:
            messagebox.showerror("Export Failed", f"An error occurred: {e}")

    root = tk.Tk()
    root.title("Text Editor")
    # root.iconphoto(False, PhotoImage(file='C:\\gui\\playstore.png'))
    trie = Trie()

    def load_dictionary(file_path):
        with open(file_path, 'r') as file:
            return [line.strip() for line in file]

    dictionary_path = "words.txt"
    dictionary = load_dictionary(dictionary_path)
    for word in dictionary:
        trie.insert(word)

    # Toolbar for font customization
    toolbar = tk.Frame(root, bg="lightgray", relief="raised", bd=2)
    toolbar.pack(side="top", fill="x")

    # Font family dropdown
    font_family_dropdown = ttk.Combobox(toolbar, values=list(font.families()), state="readonly", width=15)
    font_family_dropdown.current(font.families().index("Arial"))  # Default font family
    font_family_dropdown.pack(side="left", padx=5, pady=2)
    font_family_dropdown.bind("<<ComboboxSelected>>", lambda event: change_font_family(font_family_dropdown.get()))

    # Font size entry
    font_size_entry = ttk.Entry(toolbar, width=4)
    font_size_entry.insert(0, "12")  # Default font size
    font_size_entry.pack(side="left", padx=5, pady=2)

    # Set Font Size Button
    font_size_button = ttk.Button(toolbar, text="Set Size",
                                  command=lambda: change_font_size(int(font_size_entry.get())))
    font_size_button.pack(side="left", padx=5, pady=2)

    # Bold Button
    bold_button = ttk.Button(toolbar, text="Bold", command=toggle_bold)
    bold_button.pack(side="left", padx=5, pady=2)

    # Italic Button
    italic_button = ttk.Button(toolbar, text="Italic", command=toggle_italic)
    italic_button.pack(side="left", padx=5, pady=2)

    # Export as PDF Button
    export_pdf_button = ttk.Button(toolbar, text="Export as PDF", command=export_as_pdf)
    export_pdf_button.pack(side="left", padx=5, pady=2)

    # Statistics frame (in the same toolbar line)
    stats_frame = tk.Frame(toolbar, bg="lightgray")
    stats_frame.pack(side="right", padx=10, pady=2)

    # Arrange statistics labels horizontally
    word_count_label = tk.Label(stats_frame, text="Words: 0", bg="lightgray", font=("Arial", 8))
    word_count_label.pack(side="left", padx=5)

    char_count_label = tk.Label(stats_frame, text="Characters: 0", bg="lightgray", font=("Arial", 8))
    char_count_label.pack(side="left", padx=5)

    reading_time_label = tk.Label(stats_frame, text="Reading Time: 0min", bg="lightgray", font=("Arial", 8))
    reading_time_label.pack(side="left", padx=5)

    auto_fill_text = AutoFillText(
        root,
        trie,
        stats_callback=update_statistics,
        wrap="word",
        font=("Arial", 12)
    )
    auto_fill_text.pack(expand=True, fill="both", padx=10, pady=10)

    root.mainloop()
