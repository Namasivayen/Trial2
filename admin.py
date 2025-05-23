"""
admin.py
Admin-side features: vehicle management, booking approval/rejection.
"""
from db import create_connection
from utils import show_info, show_error

# Add or update vehicle availability
def add_or_update_vehicle(vehicle_type, model_name, count):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM vehicles WHERE type=? AND model_name=?', (vehicle_type, model_name))
    vehicle = cursor.fetchone()
    if vehicle:
        cursor.execute('UPDATE vehicles SET availability_count=? WHERE id=?', (count, vehicle[0]))
    else:
        cursor.execute('INSERT INTO vehicles (type, model_name, availability_count) VALUES (?, ?, ?)', (vehicle_type, model_name, count))
    conn.commit()
    conn.close()
    return True

# View all vehicles
def get_all_vehicles():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, type, model_name, availability_count FROM vehicles')
    vehicles = cursor.fetchall()
    conn.close()
    return vehicles

# View all bookings
def get_all_bookings():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM bookings')
    bookings = cursor.fetchall()
    conn.close()
    return bookings

# Bookings: get pending and history separately

def get_pending_bookings():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM bookings WHERE status = "Pending"')
    bookings = cursor.fetchall()
    conn.close()
    return bookings

def get_history_bookings():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM bookings WHERE status != "Pending"')
    bookings = cursor.fetchall()
    conn.close()
    return bookings

# Approve booking (only if not already approved/rejected)
def approve_booking(booking_id):
    conn = create_connection()
    cursor = conn.cursor()
    # Check booking status
    cursor.execute('SELECT status, vehicle_type, model_name FROM bookings WHERE id=?', (booking_id,))
    booking = cursor.fetchone()
    if not booking:
        conn.close()
        return False, "Booking not found."
    status, vehicle_type, model_name = booking
    if status != "Pending":
        conn.close()
        return False, "Booking already processed."
    # Find available vehicle
    cursor.execute('SELECT id, availability_count FROM vehicles WHERE type=? AND model_name=?', (vehicle_type, model_name))
    vehicle = cursor.fetchone()
    if not vehicle or vehicle[1] < 1:
        conn.close()
        return False, "No available vehicle to assign."
    # Assign vehicle and update status
    cursor.execute('UPDATE bookings SET status=?, assigned_vehicle_id=? WHERE id=?', ("Approved", vehicle[0], booking_id))
    cursor.execute('UPDATE vehicles SET availability_count=availability_count-1 WHERE id=?', (vehicle[0],))
    conn.commit()
    conn.close()
    return True, "Booking approved and vehicle assigned."

# Reject booking
def reject_booking(booking_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE bookings SET status=? WHERE id=?', ("Rejected", booking_id))
    conn.commit()
    conn.close()
    return True, "Booking rejected."
