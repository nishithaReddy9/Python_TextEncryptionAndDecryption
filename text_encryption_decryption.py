import tkinter as tk
from tkinter import ttk, messagebox


def caesar_cipher(text, key, decrypt=False):
    """Shift English letters by an integer key."""
    shift = -key if decrypt else key
    result = []

    for char in text:
        if "A" <= char <= "Z":
            result.append(chr((ord(char) - ord("A") + shift) % 26 + ord("A")))
        elif "a" <= char <= "z":
            result.append(chr((ord(char) - ord("a") + shift) % 26 + ord("a")))
        else:
            result.append(char)

    return "".join(result)


def vigenere_cipher(text, keyword, decrypt=False):
    """Encrypt or decrypt English letters using a Vigenère keyword."""
    keyword = keyword.upper()
    result = []
    key_position = 0

    for char in text:
        if "A" <= char <= "Z":
            shift = ord(keyword[key_position % len(keyword)]) - ord("A")
            if decrypt:
                shift = -shift
            result.append(chr((ord(char) - ord("A") + shift) % 26 + ord("A")))
            key_position += 1

        elif "a" <= char <= "z":
            shift = ord(keyword[key_position % len(keyword)]) - ord("A")
            if decrypt:
                shift = -shift
            result.append(chr((ord(char) - ord("a") + shift) % 26 + ord("a")))
            key_position += 1

        else:
            # Spaces, punctuation, and digits do not use a keyword character.
            result.append(char)

    return "".join(result)


def transform_text():
    message = input_text.get("1.0", tk.END).rstrip("\n")
    cipher = cipher_choice.get()
    operation = operation_choice.get()
    key = key_entry.get().strip()

    if not message.strip():
        messagebox.showerror("Input required", "Enter some text to process.")
        return

    if not key:
        messagebox.showerror("Key required", "Enter a key.")
        return

    decrypt = operation == "Decrypt"

    if cipher == "Caesar":
        try:
            numeric_key = int(key)
        except ValueError:
            messagebox.showerror(
                "Invalid key",
                "For the Caesar cipher, the key must be a whole number."
            )
            return

        result = caesar_cipher(message, numeric_key, decrypt)

    else:  # Vigenère
        if not all("A" <= char.upper() <= "Z" for char in key):
            messagebox.showerror(
                "Invalid keyword",
                "For the Vigenère cipher, use letters A-Z only."
            )
            return

        result = vigenere_cipher(message, key, decrypt)

    output_text.config(state="normal")
    output_text.delete("1.0", tk.END)
    output_text.insert("1.0", result)
    output_text.config(state="disabled")


def update_key_hint(*_):
    if cipher_choice.get() == "Caesar":
        key_label.config(text="Key (whole number):")
        key_entry.config(state="normal")
        key_hint.config(text="Example: 3")
    else:
        key_label.config(text="Keyword (letters A-Z):")
        key_entry.config(state="normal")
        key_hint.config(text="Example: LEMON")


# Create the main application window.
root = tk.Tk()
root.title("Text Encryption and Decryption")
root.geometry("700x620")
root.minsize(600, 520)

main_frame = ttk.Frame(root, padding=16)
main_frame.pack(fill="both", expand=True)
main_frame.columnconfigure(0, weight=1)
main_frame.rowconfigure(5, weight=1)
main_frame.rowconfigure(8, weight=1)

title_label = ttk.Label(
    main_frame,
    text="Text Encryption and Decryption",
    font=("Arial", 18, "bold")
)
title_label.grid(row=0, column=0, sticky="w", pady=(0, 14))

controls = ttk.Frame(main_frame)
controls.grid(row=1, column=0, sticky="ew", pady=(0, 12))
controls.columnconfigure(1, weight=1)

ttk.Label(controls, text="Cipher:").grid(row=0, column=0, sticky="w", padx=(0, 8))
cipher_choice = tk.StringVar(value="Caesar")
cipher_menu = ttk.Combobox(
    controls,
    textvariable=cipher_choice,
    values=("Caesar", "Vigenère"),
    state="readonly",
    width=18
)
cipher_menu.grid(row=0, column=1, sticky="w")
cipher_menu.bind("<<ComboboxSelected>>", update_key_hint)

ttk.Label(controls, text="Operation:").grid(row=0, column=2, sticky="w", padx=(20, 8))
operation_choice = tk.StringVar(value="Encrypt")
operation_menu = ttk.Combobox(
    controls,
    textvariable=operation_choice,
    values=("Encrypt", "Decrypt"),
    state="readonly",
    width=14
)
operation_menu.grid(row=0, column=3, sticky="w")

key_frame = ttk.Frame(main_frame)
key_frame.grid(row=2, column=0, sticky="ew", pady=(0, 12))

key_label = ttk.Label(key_frame, text="Key (whole number):")
key_label.pack(side="left")
key_entry = ttk.Entry(key_frame, width=24)
key_entry.pack(side="left", padx=8)
key_hint = ttk.Label(key_frame, text="Example: 3")
key_hint.pack(side="left")

ttk.Label(main_frame, text="Enter text:").grid(row=3, column=0, sticky="w")
input_text = tk.Text(main_frame, height=7, wrap="word")
input_text.grid(row=5, column=0, sticky="nsew", pady=(4, 12))

process_button = ttk.Button(
    main_frame,
    text="Process Text",
    command=transform_text
)
process_button.grid(row=6, column=0, sticky="w", pady=(0, 12))

ttk.Label(main_frame, text="Result:").grid(row=7, column=0, sticky="w")
output_text = tk.Text(main_frame, height=7, wrap="word", state="disabled")
output_text.grid(row=8, column=0, sticky="nsew", pady=(4, 0))

cipher_choice.trace_add("write", update_key_hint)
update_key_hint()

root.mainloop()