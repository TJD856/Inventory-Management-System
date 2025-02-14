import tkinter as tk
from tkinter import messagebox
import mysql.connector

# Function to create the emp table
def create_emp_table():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",  # Replace with your MySQL username
            password="your_password",  # Replace with your MySQL password
            database="lol1"  # Replace with your MySQL database name
        )
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS emp (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100),
                department VARCHAR(100),
                contact VARCHAR(15)
            )
        """)
        connection.commit()
        connection.close()
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")

# Function to add a new employee
def add_employee(name, department, contact):
    if not name or not department or not contact:
        messagebox.showwarning("Validation Error", "All fields are required!")
        return
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="your_password",
            database="lol1"
        )
        cursor = connection.cursor()
        cursor.execute("INSERT INTO emp (name, department, contact) VALUES (%s, %s, %s)", (name, department, contact))
        connection.commit()
        connection.close()
        messagebox.showinfo("Success", "Employee added successfully!")
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")

# Function to open the Employee Management GUI
def open_emp_gui():
    create_emp_table()  # Ensure the table exists

    emp_window = tk.Toplevel()
    emp_window.title("emp Management")
    emp_window.geometry("800x500")
    emp_window.config(bg="LavenderBlush")

    # Title Label
    title = tk.Label(emp_window, text="emp Management", font=("times new roman", 30, "bold"), bg="#010c48", fg="white")
    title.pack(side=tk.TOP, fill=tk.X)

    # Frame for employee operations
    emp_frame = tk.Frame(emp_window, bg="white", bd=3, relief=tk.RIDGE)
    emp_frame.place(x=10, y=70, width=780, height=420)

    # Labels and Entries for Employee Information
    tk.Label(emp_frame, text="Name:", font=("times new roman", 15, "bold"), bg="white").place(x=10, y=20)
    name_entry = tk.Entry(emp_frame, font=("times new roman", 15), bd=2, relief=tk.RIDGE)
    name_entry.place(x=150, y=20, width=200)

    tk.Label(emp_frame, text="Department:", font=("times new roman", 15, "bold"), bg="white").place(x=10, y=70)
    department_entry = tk.Entry(emp_frame, font=("times new roman", 15), bd=2, relief=tk.RIDGE)
    department_entry.place(x=150, y=70, width=200)

    tk.Label(emp_frame, text="Contact:", font=("times new roman", 15, "bold"), bg="white").place(x=10, y=120)
    contact_entry = tk.Entry(emp_frame, font=("times new roman", 15), bd=2, relief=tk.RIDGE)
    contact_entry.place(x=150, y=120, width=200)

    # Button to Add Employee
    add_button = tk.Button(emp_frame, text="Add Employee", font=("times new roman", 15, "bold"), bg="green", fg="white",
                           command=lambda: add_employee(name_entry.get(), department_entry.get(), contact_entry.get()))
    add_button.place(x=400, y=20, width=150, height=35)

    # Placeholder for additional functionalities (e.g., View, Update, Delete)
    tk.Label(emp_frame, text="Additional features coming soon...", font=("times new roman", 12, "italic"), bg="white").place(x=10, y=170)

    emp_window.mainloop()

# Test the GUI independently
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    open_emp_gui()
