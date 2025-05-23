# Vehicle Rental Pre-Booking System

A full-featured Python Tkinter + SQLite application for vehicle rental pre-booking, with user and admin roles.

## Features
- User & Admin authentication (username/email + password)
- User registration
- Book vehicles (Bike/Car, model, date range)
- View bookings (Pending/Approved/Rejected)
- Admin: Add/update vehicles, approve/reject bookings, assign vehicles
- Input validation, clean UI, navigation buttons

## Setup
1. Install dependencies:
   ```cmd
   pip install -r requirements.txt
   ```
2. Run the app:
   ```cmd
   python main.py
   ```

## Admin Login (default):
- Username: Nam
- Email: nam@gmail.com
- Password: nam2003

## Project Structure
- `main.py` - Main GUI
- `db.py` - Database setup & queries
- `auth.py` - Authentication logic
- `user.py` - User features
- `admin.py` - Admin features
- `utils.py` - Validation & dialogs

---
**Note:**
- The database file (`vehicle_rental.db`) is created automatically on first run.
- All data is stored locally in SQLite.
