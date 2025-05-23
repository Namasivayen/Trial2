"""
main.py
Main GUI application for Vehicle Rental Pre-Booking System.
"""
import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
from tkcalendar import DateEntry
from db import setup_database
from auth import register_user, login_user
from user import book_vehicle, get_user_bookings, BIKE_MODELS, CAR_MODELS
from admin import add_or_update_vehicle, get_all_vehicles, get_all_bookings, approve_booking, reject_booking, get_pending_bookings, get_history_bookings
from utils import show_info, show_error

# Initialize DB
setup_database()

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Vehicle Rental Pre-Booking System")
        self.geometry("700x500")  # Start in short window
        self.resizable(True, True)
        self.current_user = None
        self.is_fullscreen = False
        self.create_menu()
        self.show_login()

    def create_menu(self):
        menubar = tk.Menu(self)
        view_menu = tk.Menu(menubar, tearoff=0)
        view_menu.add_command(label="Toggle Full Screen", command=self.toggle_fullscreen)
        menubar.add_cascade(label="View", menu=view_menu)
        self.config(menu=menubar)

    def toggle_fullscreen(self):
        self.is_fullscreen = not self.is_fullscreen
        if self.is_fullscreen:
            self.state('zoomed')  # Full screen
        else:
            self.geometry("700x500")  # Back to short window

    def clear(self):
        for widget in self.winfo_children():
            widget.destroy()

    def show_login(self):
        self.clear()
        self.configure(bg='#f0f4f8')
        tk.Label(self, text="Login", font=("Arial", 20, 'bold'), bg='#f0f4f8', fg='#2d5be3').pack(pady=10)
        frame = tk.Frame(self, bg='#e3eafc', bd=2, relief='groove')
        frame.pack(pady=10)
        tk.Label(frame, text="Username or Email:", bg='#e3eafc').grid(row=0, column=0, sticky='e')
        username_entry = tk.Entry(frame, bg='#fff', fg='#222')
        username_entry.grid(row=0, column=1)
        tk.Label(frame, text="Password:", bg='#e3eafc').grid(row=1, column=0, sticky='e')
        password_entry = tk.Entry(frame, show="*", bg='#fff', fg='#222')
        password_entry.grid(row=1, column=1)
        def do_login():
            username = username_entry.get().strip()
            password = password_entry.get().strip()
            ok, user = login_user(username, password)
            if ok:
                self.current_user = user
                if user[6]:
                    self.show_admin_home()
                else:
                    self.show_user_home()
            else:
                show_error("Login Failed", user)
        tk.Button(frame, text="Login", command=do_login, bg='#2d5be3', fg='white', activebackground='#1b3a7a').grid(row=2, column=0, columnspan=2, pady=5)
        tk.Button(self, text="Register", command=self.show_register, bg='#f7b731', fg='white', activebackground='#e67e22').pack(pady=5)

    def show_register(self):
        self.clear()
        self.configure(bg='#f0f4f8')
        tk.Label(self, text="Register", font=("Arial", 20, 'bold'), bg='#f0f4f8', fg='#2d5be3').pack(pady=10)
        frame = tk.Frame(self, bg='#e3eafc', bd=2, relief='groove')
        frame.pack(pady=10)
        labels = ["Full Name", "Email", "Phone Number", "Username", "Password"]
        entries = []
        for i, label in enumerate(labels):
            tk.Label(frame, text=label+":", bg='#e3eafc').grid(row=i, column=0, sticky='e')
            entry = tk.Entry(frame, show="*" if label=="Password" else None, bg='#fff', fg='#222')
            entry.grid(row=i, column=1)
            entries.append(entry)
        def do_register():
            name, email, phone, username, password = [e.get().strip() for e in entries]
            ok, msg = register_user(name, email, phone, username, password)
            if ok:
                show_info("Success", msg)
                self.show_login()
            else:
                show_error("Registration Failed", msg)
        tk.Button(frame, text="Register", command=do_register, bg='#2d5be3', fg='white', activebackground='#1b3a7a').grid(row=5, column=0, columnspan=2, pady=5)
        tk.Button(self, text="Back", command=self.show_login, bg='#f7b731', fg='white', activebackground='#e67e22').pack(pady=5)

    def show_user_home(self):
        self.clear()
        self.configure(bg='#f0f4f8')
        tk.Label(self, text=f"Welcome, {self.current_user[1]}", font=("Arial", 16, 'bold'), bg='#f0f4f8', fg='#2d5be3').pack(pady=10)
        btn_frame = tk.Frame(self, bg='#f0f4f8')
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Book a Vehicle", width=20, command=self.show_book_vehicle, bg='#2d5be3', fg='white', activebackground='#1b3a7a').pack(pady=5)
        tk.Button(btn_frame, text="View My Bookings", width=20, command=self.show_my_bookings, bg='#f7b731', fg='white', activebackground='#e67e22').pack(pady=5)
        tk.Button(btn_frame, text="Logout", width=20, command=self.logout, bg='#eb3b5a', fg='white', activebackground='#b71c1c').pack(pady=5)

    def show_book_vehicle(self):
        self.clear()
        self.configure(bg='#f0f4f8')
        tk.Label(self, text="Book a Vehicle", font=("Arial", 18, 'bold'), bg='#f0f4f8', fg='#2d5be3').pack(pady=10)
        frame = tk.Frame(self, bg='#e3eafc', bd=2, relief='groove')
        frame.pack(pady=10)
        tk.Label(frame, text="Name:", bg='#e3eafc').grid(row=0, column=0, sticky='e')
        name_entry = tk.Entry(frame, bg='#fff', fg='#222')
        name_entry.insert(0, self.current_user[1])
        name_entry.grid(row=0, column=1)
        tk.Label(frame, text="Phone:", bg='#e3eafc').grid(row=1, column=0, sticky='e')
        phone_entry = tk.Entry(frame, bg='#fff', fg='#222')
        phone_entry.insert(0, self.current_user[3])
        phone_entry.grid(row=1, column=1)
        tk.Label(frame, text="Vehicle Type:", bg='#e3eafc').grid(row=2, column=0, sticky='e')
        type_var = tk.StringVar(value="Bike")
        type_menu = ttk.Combobox(frame, textvariable=type_var, values=["Bike", "Car"], state="readonly")
        type_menu.grid(row=2, column=1)
        tk.Label(frame, text="Model:", bg='#e3eafc').grid(row=3, column=0, sticky='e')
        model_var = tk.StringVar()
        model_menu = ttk.Combobox(frame, textvariable=model_var, values=BIKE_MODELS, state="readonly")
        model_menu.grid(row=3, column=1)
        def update_models(*args):
            if type_var.get() == "Bike":
                model_menu["values"] = BIKE_MODELS
                model_var.set(BIKE_MODELS[0])
            else:
                model_menu["values"] = CAR_MODELS
                model_var.set(CAR_MODELS[0])
        type_var.trace('w', update_models)
        update_models()
        tk.Label(frame, text="Start Date:", bg='#e3eafc').grid(row=4, column=0, sticky='e')
        start_entry = DateEntry(frame, date_pattern='yyyy-mm-dd')
        start_entry.grid(row=4, column=1)
        tk.Label(frame, text="Return Date:", bg='#e3eafc').grid(row=5, column=0, sticky='e')
        return_entry = DateEntry(frame, date_pattern='yyyy-mm-dd')
        return_entry.grid(row=5, column=1)
        def do_book():
            name = name_entry.get().strip()
            phone = phone_entry.get().strip()
            vtype = type_var.get()
            model = model_var.get()
            start = start_entry.get()
            end = return_entry.get()
            ok, msg = book_vehicle(self.current_user[0], name, phone, vtype, model, start, end)
            if ok:
                show_info("Success", msg)
                self.show_user_home()
            else:
                show_error("Booking Failed", msg)
        tk.Button(frame, text="Book", command=do_book, bg='#2d5be3', fg='white', activebackground='#1b3a7a').grid(row=6, column=0, columnspan=2, pady=5)
        tk.Button(self, text="Back", command=self.show_user_home, bg='#f7b731', fg='white', activebackground='#e67e22').pack(pady=5)

    def show_my_bookings(self):
        self.clear()
        self.configure(bg='#f0f4f8')
        tk.Label(self, text="My Bookings", font=("Arial", 18, 'bold'), bg='#f0f4f8', fg='#2d5be3').pack(pady=10)
        bookings = get_user_bookings(self.current_user[0])
        cols = ("ID", "Type", "Model", "Start", "Return", "Status")
        tree = ttk.Treeview(self, columns=cols, show='headings')
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 10, 'bold'), background="#2d5be3", foreground="white")
        style.configure("Treeview", font=("Arial", 10), rowheight=25)
        for col in cols:
            tree.heading(col, text=col)
        for b in bookings:
            status = b[5]
            if status.lower() == 'pending':
                status_display = 'Waiting'
                tag = 'pending'
            elif status.lower() == 'approved':
                status_display = 'Approved'
                tag = 'approved'
            elif status.lower() == 'rejected':
                status_display = 'Rejected'
                tag = 'rejected'
            else:
                status_display = status
                tag = ''
            tree.insert('', 'end', values=(b[0], b[1], b[2], b[3], b[4], status_display), tags=(tag,))
        tree.tag_configure('pending', background='#fffbe6')
        tree.tag_configure('approved', background='#e6ffed')
        tree.tag_configure('rejected', background='#ffe6e6')
        tree.pack(pady=10)
        tk.Button(self, text="Back", command=self.show_user_home, bg='#f7b731', fg='white', activebackground='#e67e22').pack(pady=5)

    def show_admin_home(self):
        self.clear()
        self.configure(bg='#f0f4f8')
        tk.Label(self, text=f"Admin: {self.current_user[1]}", font=("Arial", 16, 'bold'), bg='#f0f4f8', fg='#2d5be3').pack(pady=10)
        btn_frame = tk.Frame(self, bg='#f0f4f8')
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="View Vehicle List", width=25, command=self.show_vehicle_list, bg='#2d5be3', fg='white', activebackground='#1b3a7a').pack(pady=5)
        tk.Button(btn_frame, text="Add/Update Vehicle", width=25, command=self.show_add_vehicle, bg='#f7b731', fg='white', activebackground='#e67e22').pack(pady=5)
        tk.Button(btn_frame, text="View All Bookings", width=25, command=self.show_all_bookings, bg='#20bf6b', fg='white', activebackground='#145a32').pack(pady=5)
        tk.Button(btn_frame, text="Logout", width=25, command=self.logout, bg='#eb3b5a', fg='white', activebackground='#b71c1c').pack(pady=5)

    def show_vehicle_list(self):
        self.clear()
        self.configure(bg='#f0f4f8')
        tk.Label(self, text="Vehicle List", font=("Arial", 18, 'bold'), bg='#f0f4f8', fg='#2d5be3').pack(pady=10)
        vehicles = get_all_vehicles()
        cols = ("ID", "Type", "Model", "Available")
        tree = ttk.Treeview(self, columns=cols, show='headings')
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 10, 'bold'), background="#2d5be3", foreground="white")
        style.configure("Treeview", font=("Arial", 10), rowheight=25)
        for col in cols:
            tree.heading(col, text=col)
        for v in vehicles:
            tree.insert('', 'end', values=v)
        tree.pack(pady=10)
        tk.Button(self, text="Back", command=self.show_admin_home, bg='#f7b731', fg='white', activebackground='#e67e22').pack(pady=5)

    def show_add_vehicle(self):
        self.clear()
        self.configure(bg='#f0f4f8')
        tk.Label(self, text="Add/Update Vehicle", font=("Arial", 18, 'bold'), bg='#f0f4f8', fg='#2d5be3').pack(pady=10)
        frame = tk.Frame(self, bg='#e3eafc', bd=2, relief='groove')
        frame.pack(pady=10)
        tk.Label(frame, text="Type:", bg='#e3eafc').grid(row=0, column=0, sticky='e')
        type_var = tk.StringVar(value="Bike")
        type_menu = ttk.Combobox(frame, textvariable=type_var, values=["Bike", "Car"], state="readonly")
        type_menu.grid(row=0, column=1)
        tk.Label(frame, text="Model:", bg='#e3eafc').grid(row=1, column=0, sticky='e')
        model_var = tk.StringVar()
        model_menu = ttk.Combobox(frame, textvariable=model_var, values=BIKE_MODELS, state="readonly")
        model_menu.grid(row=1, column=1)
        def update_models(*args):
            if type_var.get() == "Bike":
                model_menu["values"] = BIKE_MODELS
                model_var.set(BIKE_MODELS[0])
            else:
                model_menu["values"] = CAR_MODELS
                model_var.set(CAR_MODELS[0])
        type_var.trace('w', update_models)
        update_models()
        tk.Label(frame, text="Availability Count:", bg='#e3eafc').grid(row=2, column=0, sticky='e')
        count_entry = tk.Entry(frame, bg='#fff', fg='#222')
        count_entry.grid(row=2, column=1)
        def do_add():
            vtype = type_var.get()
            model = model_var.get()
            try:
                count = int(count_entry.get())
                if count < 0:
                    raise ValueError
            except:
                show_error("Invalid Input", "Availability count must be a non-negative integer.")
                return
            add_or_update_vehicle(vtype, model, count)
            show_info("Success", "Vehicle info updated.")
            self.show_admin_home()
        tk.Button(frame, text="Add/Update", command=do_add, bg='#2d5be3', fg='white', activebackground='#1b3a7a').grid(row=3, column=0, columnspan=2, pady=5)
        tk.Button(self, text="Back", command=self.show_admin_home, bg='#f7b731', fg='white', activebackground='#e67e22').pack(pady=5)

    def show_all_bookings(self):
        self.clear()
        self.configure(bg='#f0f4f8')
        tk.Label(self, text="Pending Bookings", font=("Arial", 16, 'bold'), bg='#f0f4f8', fg='#2d5be3').pack(pady=5)
        pending = get_pending_bookings()
        cols = ("ID", "UserID", "Type", "Model", "Start", "Return", "Status", "AssignedVehicleID")
        tree_pending = ttk.Treeview(self, columns=cols, show='headings', height=5)
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 10, 'bold'), background="#2d5be3", foreground="white")
        style.configure("Treeview", font=("Arial", 10), rowheight=25)
        for col in cols:
            tree_pending.heading(col, text=col)
        for b in pending:
            tree_pending.insert('', 'end', values=b)
        tree_pending.pack(pady=5)
        def approve_selected():
            selected = tree_pending.selection()
            if not selected:
                show_error("Error", "Select a booking to approve.")
                return
            booking_id = tree_pending.item(selected[0])['values'][0]
            ok, msg = approve_booking(booking_id)
            if ok:
                show_info("Success", msg)
                self.show_all_bookings()
            else:
                show_error("Error", msg)
        def reject_selected():
            selected = tree_pending.selection()
            if not selected:
                show_error("Error", "Select a booking to reject.")
                return
            booking_id = tree_pending.item(selected[0])['values'][0]
            ok, msg = reject_booking(booking_id)
            if ok:
                show_info("Success", msg)
                self.show_all_bookings()
            else:
                show_error("Error", msg)
        btn_frame = tk.Frame(self, bg='#f0f4f8')
        btn_frame.pack(pady=2)
        tk.Button(btn_frame, text="Approve", command=approve_selected, bg='#20bf6b', fg='white', activebackground='#145a32').pack(side='left', padx=5)
        tk.Button(btn_frame, text="Reject", command=reject_selected, bg='#eb3b5a', fg='white', activebackground='#b71c1c').pack(side='left', padx=5)
        # History section
        tk.Label(self, text="Booking History", font=("Arial", 16, 'bold'), bg='#f0f4f8', fg='#2d5be3').pack(pady=5)
        history = get_history_bookings()
        tree_history = ttk.Treeview(self, columns=cols, show='headings', height=7)
        for col in cols:
            tree_history.heading(col, text=col)
        for b in history:
            tree_history.insert('', 'end', values=b)
        tree_history.pack(pady=5)
        tk.Button(self, text="Back", command=self.show_admin_home, bg='#f7b731', fg='white', activebackground='#e67e22').pack(pady=5)

    def logout(self):
        self.current_user = None
        self.show_login()

if __name__ == "__main__":
    try:
        from tkcalendar import DateEntry
    except ImportError:
        import os
        os.system('pip install tkcalendar')
        from tkcalendar import DateEntry
    app = App()
    app.mainloop()
