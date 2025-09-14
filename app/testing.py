# words = [
#     "apple",
#     "banana",
#     "cherry",
#     "dragon",
#     "elephant",
#     "forest",
#     "guitar",
#     "honey",
#     "island",
#     "jungle",
#     "kangaroo",
#     "lemon",
#     "mountain",
#     "nectar",
#     "ocean",
#     "piano",
#     "quartz",
#     "river",
#     "sunset",
#     "tiger",
#     "umbrella",
# ]

import tkinter as tk
from tkinter import simpledialog

# def select_word_interface(words):
#     selected_word = {'value': None}

#     def on_select():
#         selection = listbox.curselection()
#         if selection:
#             selected_word['value'] = words[selection[0]]
#             root.destroy()

#     def on_cancel():
#         selected_word['value'] = None
#         root.destroy()

#     root = tk.Tk()
#     root.title("Select a Word")
#     root.geometry("300x300")
#     root.resizable(False, False)

#     listbox = tk.Listbox(root, height=10, selectmode=tk.SINGLE)
#     for word in words:
#         listbox.insert(tk.END, word)
#     listbox.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

#     button_frame = tk.Frame(root)
#     button_frame.pack(pady=10)

#     select_btn = tk.Button(button_frame, text="Select", command=on_select)
#     select_btn.pack(side=tk.LEFT, padx=5)

#     cancel_btn = tk.Button(button_frame, text="Cancel", command=on_cancel)
#     cancel_btn.pack(side=tk.LEFT, padx=5)c
#     # Ensure the window is brought to the front and focused
#     root.lift()
#     root.attributes('-topmost', True)
#     root.after_idle(root.attributes, '-topmost', False)
#     root.focus_force()

#     root.mainloop()
#     return selected_word['value']


# selected = select_word_interface(words)
# if selected is None:
#     print("Operation cancelled.")
# else:
#     print("Selected OP: ", selected)
    # INSERT_YOUR_CODE
def get_credentials_interface():
    credentials = {'username': None, 'password': None}

    def on_submit():
        credentials['username'] = username_entry.get()
        credentials['password'] = password_entry.get()
        cred_root.destroy()

    def on_cancel():
        credentials['username'] = None
        credentials['password'] = None
        cred_root.destroy()

    cred_root = tk.Tk()
    cred_root.title("Enter Credentials")
    cred_root.geometry("300x180")
    cred_root.resizable(False, False)

    frame = tk.Frame(cred_root)
    frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

    tk.Label(frame, text="Username:").grid(row=0, column=0, sticky="e", pady=5)
    username_entry = tk.Entry(frame)
    username_entry.grid(row=0, column=1, pady=5)

    tk.Label(frame, text="Password:").grid(row=1, column=0, sticky="e", pady=5)
    password_entry = tk.Entry(frame, show="*")
    password_entry.grid(row=1, column=1, pady=5)

    button_frame = tk.Frame(cred_root)
    button_frame.pack(pady=10)

    submit_btn = tk.Button(button_frame, text="Submit", command=on_submit)
    submit_btn.pack(side=tk.LEFT, padx=5)

    cancel_btn = tk.Button(button_frame, text="Cancel", command=on_cancel)
    cancel_btn.pack(side=tk.LEFT, padx=5)

    cred_root.lift()
    cred_root.attributes('-topmost', True)
    cred_root.after_idle(cred_root.attributes, '-topmost', False)
    cred_root.focus_force()

    cred_root.mainloop()
    return credentials

# Example usage:
creds = get_credentials_interface()
if creds['username'] is None or creds['password'] is None:
    print("Credentials input cancelled.")
else:
    print("Username:", creds['username'])
    print("Password:", creds['password'])
    # You can use creds['username'] and creds['password'] in your program
