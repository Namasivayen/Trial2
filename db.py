"""
db.py
Handles all database operations for the Vehicle Rental Pre-Booking System.
"""
import sqlite3
from sqlite3 import Error

DB_NAME = 'vehicle_rental.db'

# Initial admin credentials
ADMIN = {
    'name': 'Nam',
    'email': 'nam@gmail.com',
    'phone': '7708416954',
    'username': 'Nam',
    'password': 'nam2003',
    'is_admin': 1
}

def create_connection():
    """Create a database connection to the SQLite database."""
    conn = None
    try:
        conn = sqlite3.connect(DB_NAME)
    except Error as e:
        print(e)
    return conn

def setup_database():
    """Create tables and insert initial admin if not exists."""
    conn = create_connection()
    cursor = conn.cursor()
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            phone TEXT NOT NULL,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            is_admin INTEGER DEFAULT 0
        )
    ''')
    # Create vehicles table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vehicles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL,
            model_name TEXT NOT NULL,
            availability_count INTEGER NOT NULL
        )
    ''')
    # Create bookings table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            vehicle_type TEXT NOT NULL,
            model_name TEXT NOT NULL,
            start_date TEXT NOT NULL,
            return_date TEXT NOT NULL,
            status TEXT NOT NULL,
            assigned_vehicle_id INTEGER,
            FOREIGN KEY(user_id) REFERENCES users(id),
            FOREIGN KEY(assigned_vehicle_id) REFERENCES vehicles(id)
        )
    ''')
    # Insert initial admin if not exists
    cursor.execute('SELECT * FROM users WHERE username=?', (ADMIN['username'],))
    if not cursor.fetchone():
        cursor.execute('''
            INSERT INTO users (name, email, phone, username, password, is_admin)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (ADMIN['name'], ADMIN['email'], ADMIN['phone'], ADMIN['username'], ADMIN['password'], ADMIN['is_admin']))
    conn.commit()
    conn.close()

def get_user_by_username_or_email(username_or_email):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username=? OR email=?', (username_or_email, username_or_email))
    user = cursor.fetchone()
    conn.close()
    return user

# ...other db functions for CRUD operations will be added as needed...
