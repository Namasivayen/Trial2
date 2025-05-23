"""
auth.py
Handles authentication and registration logic.
"""
from db import get_user_by_username_or_email, create_connection
from utils import validate_email, validate_phone

# Registration function
def register_user(name, email, phone, username, password):
    if not name or not email or not phone or not username or not password:
        return False, "All fields are required."
    if not validate_email(email):
        return False, "Invalid email format."
    if not validate_phone(phone):
        return False, "Invalid phone number."
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO users (name, email, phone, username, password, is_admin) VALUES (?, ?, ?, ?, ?, 0)',
                       (name, email, phone, username, password))
        conn.commit()
        return True, "Registration successful!"
    except Exception as e:
        return False, f"Registration failed: {str(e)}"
    finally:
        conn.close()

# Login function
def login_user(username_or_email, password):
    user = get_user_by_username_or_email(username_or_email)
    if user and user[5] == password:
        return True, user
    return False, "Invalid credentials."
