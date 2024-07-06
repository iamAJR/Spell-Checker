import requests
from tkinter import *
from tkinter import messagebox
import difflib
from text_speech import say
import threading
from MUTLIcheck import  check

def load_dictionary(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file]

def save_to_dictionary(file_path, word):
    with open(file_path, 'a') as file:
        file.write(word + "\n")

def fetch_definition(word):
    api_key = 'bb06a07b-96c5-4e3d-b4c4-1f15343b190c'
    url = f"https://www.dictionaryapi.com/api/v3/references/collegiate/json/{word}?key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data and isinstance(data[0], dict):
            return data[0].get('shortdef', ["No definition found"])
    return ["No definition found"]

def fetch_synonyms(word):
    api_key = 'cdabdf20-a184-4746-afd8-6186e69b63d0'
    url = f"https://www.dictionaryapi.com/api/v3/references/thesaurus/json/{word}?key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data and isinstance(data[0], dict):
            synonyms = []
            for meta in data[0].get('meta', {}).get('syns', []):
                synonyms.extend(meta)
            return synonyms
    return ["No synonyms found"]

def checker(word, dict_list):
    suggestions = difflib.get_close_matches(word, dict_list, n=8, cutoff=0.6)
    return [(suggestion, 0) for suggestion in suggestions]

def check_spelling():
    word = input_text.get()
    suggestions = checker(word, dictionary)
    suggestion_list = [suggestion[0] for suggestion in suggestions]
    listbox.delete(0, END)
    for suggestion in suggestion_list:
        listbox.insert(END, suggestion)

def threaded_say(selected_word):
    threading.Thread(target=say, args=(selected_word,), daemon=True).start()

def show_definition_and_synonyms(event):
    if listbox.curselection():
        selected_word = listbox.get(listbox.curselection()[0])
        threaded_say(selected_word)

        definition = fetch_definition(selected_word)
        synonyms = fetch_synonyms(selected_word)

        definition_text.config(state=NORMAL)
        definition_text.delete(1.0, END)
        definition_text.insert(END, '\n'.join(definition))
        definition_text.config(state=DISABLED)

        synonyms_text.config(state=NORMAL)
        synonyms_text.delete(1.0, END)
        synonyms_text.insert(END, ', '.join(synonyms))
        synonyms_text.config(state=DISABLED)

        output_frame.pack_forget()
        definition_frame.pack(pady=10)

def add_to_dictionary():
    word = input_text.get()
    if word and word not in dictionary:
        dictionary.append(word)
        save_to_dictionary(dictionary_path, word)
        messagebox.showinfo("Success", f"'{word}' has been added to the dictionary!")
    else:
        messagebox.showerror("Error", "Word already in the dictionary.")

def show_suggestions():
    definition_frame.pack_forget()
    output_frame.pack(pady=20)

def show_initial(event=None):
    hide_frames()
    header_frame.pack(fill='x')
    input_frame.pack(pady=20)
    output_frame.pack(pady=30)

def multi_line_text_view(event=None):
    hide_frames()
    multi_line_text.pack(fill='both', expand=True)

def hide_frames():
    header_frame.forget()
    input_frame.forget()
    output_frame.forget()
    multi_line_text.forget()

def multi_check_spelling():
    # Placeholder for spell check logic
    text = entry_text.get("1.0", END).strip()
    if not text:
        messagebox.showwarning("Warning", "Please enter text to check.")
        return

    # Example of checking for a misspelled word
    words = text.split()

    word_count.config(text=f"Word count: {len(words)}")

def clear_text():
    entry_text.delete('1.0', END)
    mlti_listbox.delete(0, END)
    word_count.config(text="Word count: 0")

def show_suggestions_mlti(event):
    # Get the index of the cursor position
    index = entry_text.index(f"@{event.x},{event.y}")

    # Get the start and end indices of the word
    word_start = entry_text.index(f"{index} wordstart")
    word_end = entry_text.index(f"{index} wordend")

    # Extract the word
    selected_word = entry_text.get(word_start, word_end).strip()

    # Get suggestions
    suggestions = check(selected_word, dictionary)
    suggestion_list = [suggestion[0] for suggestion in suggestions]

    # Clear the listbox before updating it with new suggestions
    mlti_listbox.delete(0, END)

    # Add suggestions to the listbox
    for suggestion in suggestion_list:
        mlti_listbox.insert(END, suggestion)

#root
root = Tk()
root.title("SPELL CHECKER")
root.geometry("800x700")
root.config(background="#1A1A1A")
root.iconphoto(False, PhotoImage(file='C:\\gui\\playstore.png'))

dictionary_path = "words.txt"
dictionary = load_dictionary(dictionary_path)

#header
header_frame = Frame(root, bg="#333333", bd=5)
header_frame.pack(fill="x")

heading = Label(header_frame, text="Spell Checker", font=("Helvetica", 30, "bold"), bg="#333333", fg="#FFD700")
heading.pack()

#input
input_frame = Frame(root, bg="#1A1A1A")
input_frame.pack(pady=20)

input_label = Label(input_frame, text="Enter Word:", font=("Helvetica", 20), bg="#1A1A1A", fg="#FFFFFF")
input_label.grid(row=0, column=0, padx=10)

multi_line = Button(input_frame, text="Multi Line", font=("Helvetica", 20, "bold"), bg="orange", fg="#FFFFFF", command=multi_line_text_view)
multi_line.grid(row=2, column=0)

input_text = Entry(input_frame, justify="center", width=15, font=("poppins", 25), bg="#FFFFFF", fg="#000000", border=2)
input_text.grid(row=0, column=1, padx=10)
input_text.focus()

button_frame = Frame(input_frame, bg="#1A1A1A")
button_frame.grid(row=0, column=2, padx=10)

button_check = Button(button_frame, text="Check", width=10, font=("arial", 20, "bold"), fg="#FFFFFF", bg="#FF4500",
                      command=check_spelling)
button_check.pack(pady=5)

#nextmultilinepg
# Multi-line text frame
multi_line_text = Frame(root, bg="#1A1A1A")

# Back button
back_button = Button(multi_line_text, text='Back', font=("Helvetica", 15, "bold"), bg="#333333", fg="#FFD700", command=show_initial)
back_button.grid(row=0, column=0, padx=20, pady=20, sticky="nw")

# Text entry section
entry_frame = Frame(multi_line_text, bg="#1A1A1A")
entry_frame.grid(row=1, column=0, padx=10, pady=10, columnspan=2, sticky="nsew")

entry_label = Label(entry_frame, text="Enter Text:", font=("Helvetica", 20, "bold"), bg="#1A1A1A", fg="#FFFFFF")
entry_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

entry_text = Text(entry_frame, font=("Poppins", 20), width=60, height=10, bg="#FFFFFF", fg="#000000", border=2)
entry_text.grid(row=1, column=0, padx=10, pady=10, columnspan=2, sticky="w")

# Suggestions section
suggestions_frame = Frame(multi_line_text, bg="#1A1A1A")
suggestions_frame.grid(row=2, column=0, padx=10, pady=10, columnspan=2, sticky="nsew")

suggestions_label = Label(suggestions_frame, text="Suggestions:", font=("Helvetica", 20, "bold"), bg="#1A1A1A", fg="#FFFFFF")
suggestions_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

mlti_listbox = Listbox(suggestions_frame, font=("Poppins", 20), width=30, height=10, bg="#FFFFFF", fg="#000000", border=2)
mlti_listbox.grid(row=1, column=0, padx=25, pady=35)

word_count = Label(multi_line_text, text="Word count: 0", font=("Helvetica", 15, "bold"), bg="#1A1A1A", fg="#FFFFFF")
word_count.grid(row=3, column=0, padx=10, pady=10, sticky="w")

clear_button = Button(multi_line_text, text="Clear", font=("Helvetica", 15, "bold"), bg="#FF4500", fg="#FFFFFF", command=clear_text)
clear_button.grid(row=3, column=1, padx=10, pady=10, sticky="e")

entry_text.bind("<ButtonRelease-1>", show_suggestions_mlti)

output_frame = Frame(root, bg="#1A1A1A")
output_frame.pack(pady=30)

listbox = Listbox(output_frame, width=30, height=10, font=("poppins", 20), bg="#FFFFFF", fg="#000000", border=2)
listbox.pack(padx=10, pady=10)
listbox.bind("<Double-Button-1>", show_definition_and_synonyms)

button_add = Button(output_frame, text="Add to Dictionary", font=("arial", 20, "bold"), fg="#FFFFFF", bg="#00C957",
                    command=add_to_dictionary)
button_add.pack(pady=10)

definition_frame = Frame(root, bg="#1A1A1A")

definition_label = Label(definition_frame, text="Definition:", font=("Helvetica", 20, "bold"), bg="#1A1A1A", fg="#FFFFFF")
definition_label.pack(pady=10)

definition_text = Text(definition_frame, height=5, width=60, font=("poppins", 20), bg="#FFFFFF", fg="#000000", border=2)
definition_text.pack(padx=10, pady=10)
definition_text.config(state=DISABLED)

synonyms_label = Label(definition_frame, text="Synonyms:", font=("Helvetica", 20, "bold"), bg="#1A1A1A", fg="#FFFFFF")
synonyms_label.pack(pady=10)

synonyms_text = Text(definition_frame, height=5, width=60, font=("poppins", 20), bg="#FFFFFF", fg="#000000", border=2)
synonyms_text.pack(padx=10, pady=10)
synonyms_text.config(state=DISABLED)

back_button = Button(definition_frame, text="Back", width=10, font=("arial", 20, "bold"), fg="#FFFFFF", bg="#333333",
                     command=show_suggestions)
back_button.pack(pady=10)

root.bind("<BackSpace>", show_initial)  # Bind Backspace key to show_initial

# Bind Backspace key to show_initial in single-line mode
input_text.bind("<BackSpace>", show_initial)

# Bind Backspace key to multi_line_text_view in multi-line mode
entry_text.bind("<BackSpace>", show_initial)

root.mainloop()
