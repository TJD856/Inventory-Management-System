from tkinter import *
from tkinter import ttk, messagebox
import mysql.connector

# Database Connection
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="your_password",
        database="lol1"
    )

# Function to Add Supplier
def add_supplier():
    if name_var.get() == "" or contact_var.get() == "" or email_var.get() == "" or address_var.get() == "":
        messagebox.showerror("Error", "All fields are required!")
    else:
        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO suppliers (name, contact, email, address) VALUES (%s, %s, %s, %s)",
                           (name_var.get(), contact_var.get(), email_var.get(), address_var.get()))
            conn.commit()
            conn.close()
            fetch_suppliers()
            clear_fields()
            messagebox.showinfo("Success", "Supplier added successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Error due to: {e}")

# Function to Fetch Suppliers
def fetch_suppliers():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM suppliers")
    rows = cursor.fetchall()
    supplier_table.delete(*supplier_table.get_children())
    for row in rows:
        supplier_table.insert("", END, values=row)
    conn.close()

# Function to Select Supplier from Table
def select_supplier(event):
    selected_row = supplier_table.focus()
    content = supplier_table.item(selected_row)
    row = content["values"]
    if row:
        id_var.set(row[0])
        name_var.set(row[1])
        contact_var.set(row[2])
        email_var.set(row[3])
        address_var.set(row[4])

# Function to Update Supplier
def update_supplier():
    if id_var.get() == "":
        messagebox.showerror("Error", "Please select a supplier to update!")
    else:
        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("UPDATE suppliers SET name=%s, contact=%s, email=%s, address=%s WHERE id=%s",
                           (name_var.get(), contact_var.get(), email_var.get(), address_var.get(), id_var.get()))
            conn.commit()
            conn.close()
            fetch_suppliers()
            clear_fields()
            messagebox.showinfo("Success", "Supplier updated successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Error due to: {e}")

# Function to Delete Supplier
def delete_supplier():
    if id_var.get() == "":
        messagebox.showerror("Error", "Please select a supplier to delete!")
    else:
        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM suppliers WHERE id=%s", (id_var.get(),))
            conn.commit()
            conn.close()
            fetch_suppliers()
            clear_fields()
            messagebox.showinfo("Success", "Supplier deleted successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Error due to: {e}")

# Function to Clear Fields
def clear_fields():
    id_var.set("")
    name_var.set("")
    contact_var.set("")
    email_var.set("")
    address_var.set("")

# Create Main Supplier Window
supplier_window = Tk()
supplier_window.title("Supplier Management")
supplier_window.geometry("800x500")
supplier_window.config(bg="LightBlue")
supplier_window.attributes("-topmost", True)

# Title Label
title_label = Label(supplier_window, text="Supplier Management", font=("Arial", 20, "bold"), bg="DarkBlue", fg="white")
title_label.pack(side=TOP, fill=X)

# Variables
id_var = StringVar()
name_var = StringVar()
contact_var = StringVar()
email_var = StringVar()
address_var = StringVar()

# Supplier Form
form_frame = Frame(supplier_window, bg="LightBlue")
form_frame.place(x=20, y=50, width=350, height=400)

Label(form_frame, text="Supplier Name:", font=("Arial", 12, "bold"), bg="LightBlue").grid(row=0, column=0, pady=10, sticky="w")
Entry(form_frame, textvariable=name_var, font=("Arial", 12)).grid(row=0, column=1, pady=10)

Label(form_frame, text="Contact:", font=("Arial", 12, "bold"), bg="LightBlue").grid(row=1, column=0, pady=10, sticky="w")
Entry(form_frame, textvariable=contact_var, font=("Arial", 12)).grid(row=1, column=1, pady=10)

Label(form_frame, text="Email:", font=("Arial", 12, "bold"), bg="LightBlue").grid(row=2, column=0, pady=10, sticky="w")
Entry(form_frame, textvariable=email_var, font=("Arial", 12)).grid(row=2, column=1, pady=10)

Label(form_frame, text="Address:", font=("Arial", 12, "bold"), bg="LightBlue").grid(row=3, column=0, pady=10, sticky="w")
Entry(form_frame, textvariable=address_var, font=("Arial", 12)).grid(row=3, column=1, pady=10)

# Buttons
btn_frame = Frame(form_frame, bg="LightBlue")
btn_frame.grid(row=4, columnspan=2, pady=10)

Button(btn_frame, text="Add", font=("Arial", 12), bg="Green", fg="white", command=add_supplier).grid(row=0, column=0, padx=5)
Button(btn_frame, text="Update", font=("Arial", 12), bg="Blue", fg="white", command=update_supplier).grid(row=0, column=1, padx=5)
Button(btn_frame, text="Delete", font=("Arial", 12), bg="Red", fg="white", command=delete_supplier).grid(row=0, column=2, padx=5)
Button(btn_frame, text="Clear", font=("Arial", 12), bg="Gray", fg="white", command=clear_fields).grid(row=0, column=3, padx=5)

# Supplier Table
table_frame = Frame(supplier_window)
table_frame.place(x=400, y=50, width=380, height=400)

columns = ("ID", "Name", "Contact", "Email", "Address")
supplier_table = ttk.Treeview(table_frame, columns=columns, show="headings")
supplier_table.column("ID", width=50)
supplier_table.column("Name", width=100)
supplier_table.column("Contact", width=100)
supplier_table.column("Email", width=100)
supplier_table.column("Address", width=100)
supplier_table.heading("ID", text="ID")
supplier_table.heading("Name", text="Name")
supplier_table.heading("Contact", text="Contact")
supplier_table.heading("Email", text="Email")
supplier_table.heading("Address", text="Address")
supplier_table.bind("<ButtonRelease-1>", select_supplier)
supplier_table.pack(fill=BOTH, expand=True)

# Fetch existing suppliers
fetch_suppliers()

# Run the Tkinter loop
supplier_window.mainloop()
