# gui_password_analyzer.py
import tkinter as tk
from tkinter import messagebox, filedialog
from zxcvbn import zxcvbn
import os

LEET_MAP = {
    'a': ['a', '@', '4'],
    'e': ['e', '3'],
    'i': ['i', '1', '!'],
    'o': ['o', '0'],
    's': ['s', '$', '5'],
    't': ['t', '7']
}

def analyze_password(password):
    analysis = zxcvbn(password)
    result = f"Password: {password}\n"
    result += f"Score: {analysis['score']} / 4\n"
    result += f"Guesses: {analysis['guesses']}\n"
    result += f"Crack time: {analysis['crack_times_display']['offline_slow_hashing_1e4_per_second']}\n"
    result += f"Feedback: {analysis['feedback']['warning'] or 'None'}"
    return result

def generate_variants(word):
    variants = ['']
    for char in word.lower():
        options = LEET_MAP.get(char, [char])
        variants = [prefix + opt for prefix in variants for opt in options]
    return list(set(variants))

def generate_wordlist(inputs, years=["", "2024", "123"]):
    base_words = []
    for item in inputs:
        base_words.extend(generate_variants(item))
    wordlist = set()
    for word in base_words:
        for year in years:
            wordlist.add(word + year)
            wordlist.add(year + word)
    return sorted(wordlist)

def save_wordlist(wordlist, filename):
    with open(filename, 'w') as f:
        for word in wordlist:
            f.write(word + '\n')

def analyze_and_generate():
    password = password_entry.get()
    inputs = input_entry.get().split()
    if not password and not inputs:
        messagebox.showwarning("Input Required", "Enter a password and/or custom inputs.")
        return
    output = ""
    if password:
        output += analyze_password(password) + "\n\n"
    if inputs:
        wordlist = generate_wordlist(inputs)
        filepath = filedialog.asksaveasfilename(defaultextension=".txt", title="Save Wordlist As")
        if filepath:
            save_wordlist(wordlist, filepath)
            output += f"Wordlist saved: {filepath} (Total: {len(wordlist)} words)"
    result_text.delete("1.0", tk.END)
    result_text.insert(tk.END, output)

# GUI Setup
root = tk.Tk()
root.title("Password Strength & Wordlist Generator")
root.geometry("600x400")

tk.Label(root, text="Password:").pack(pady=5)
password_entry = tk.Entry(root, width=50, show="*")
password_entry.pack()

tk.Label(root, text="Custom Inputs (e.g., names, dates, pets):").pack(pady=5)
input_entry = tk.Entry(root, width=50)
input_entry.pack()

tk.Button(root, text="Analyze & Generate Wordlist", command=analyze_and_generate).pack(pady=10)

result_text = tk.Text(root, height=10, wrap="word")
result_text.pack(pady=10)

root.mainloop()
