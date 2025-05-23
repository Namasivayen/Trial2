"""
user.py
User-side features: booking, viewing bookings.
"""
from db import create_connection
from utils import show_info, show_error

BIKE_MODELS = ["Hero", "Honda", "Yamaha", "KTM", "Royal Enfield"]
CAR_MODELS = ["Suzuki", "Honda", "Toyota", "Volkswagen", "Hyundai"]

# Book a vehicle
def book_vehicle(user_id, name, phone, vehicle_type, model_name, start_date, return_date):
    conn = create_connection()
    cursor = conn.cursor()
    # Check vehicle availability
    cursor.execute('SELECT id, availability_count FROM vehicles WHERE type=? AND model_name=?', (vehicle_type, model_name))
    vehicle = cursor.fetchone()
    if not vehicle or vehicle[1] < 1:
        conn.close()
        return False, "Selected vehicle is not available."
    # Insert booking with Pending status
    cursor.execute('''
        INSERT INTO bookings (user_id, vehicle_type, model_name, start_date, return_date, status, assigned_vehicle_id)
        VALUES (?, ?, ?, ?, ?, ?, NULL)
    ''', (user_id, vehicle_type, model_name, start_date, return_date, "Pending"))
    conn.commit()
    conn.close()
    return True, "Booking submitted and is pending approval."

# View user's bookings
def get_user_bookings(user_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, vehicle_type, model_name, start_date, return_date, status FROM bookings WHERE user_id=?', (user_id,))
    bookings = cursor.fetchall()
    conn.close()
    return bookings
