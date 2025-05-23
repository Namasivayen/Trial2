"""
utils.py
Utility functions for validation and message dialogs.
"""
import re
from tkinter import messagebox

def validate_email(email):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email)

def validate_phone(phone):
    return phone.isdigit() and len(phone) == 10

def show_info(title, message):
    messagebox.showinfo(title, message)

def show_error(title, message):
    messagebox.showerror(title, message)
