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

# Function to Add Sale
def add_sale():
    if product_id_var.get() == "" or quantity_var.get() == "" or total_price_var.get() == "" or date_var.get() == "":
        messagebox.showerror("Error", "All fields are required!")
    else:
        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO sales (product_id, quantity, total_price, sale_date) VALUES (%s, %s, %s, %s)",
                           (product_id_var.get(), quantity_var.get(), total_price_var.get(), date_var.get()))
            conn.commit()
            conn.close()
            fetch_sales()
            clear_fields()
            messagebox.showinfo("Success", "Sale added successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Error due to: {e}")

# Function to Fetch Sales
def fetch_sales():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT s.id, p.name, s.quantity, s.total_price, s.sale_date FROM sales s INNER JOIN products p ON s.product_id = p.id")
    rows = cursor.fetchall()
    sales_table.delete(*sales_table.get_children())
    for row in rows:
        sales_table.insert("", END, values=row)
    conn.close()

# Function to Select Sale from Table
def select_sale(event):
    selected_row = sales_table.focus()
    content = sales_table.item(selected_row)
    row = content["values"]
    if row:
        id_var.set(row[0])
        product_id_var.set(row[1])
        quantity_var.set(row[2])
        total_price_var.set(row[3])
        date_var.set(row[4])

# Function to Update Sale
def update_sale():
    if id_var.get() == "":
        messagebox.showerror("Error", "Please select a sale to update!")
    else:
        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("UPDATE sales SET product_id=%s, quantity=%s, total_price=%s, sale_date=%s WHERE id=%s",
                           (product_id_var.get(), quantity_var.get(), total_price_var.get(), date_var.get(), id_var.get()))
            conn.commit()
            conn.close()
            fetch_sales()
            clear_fields()
            messagebox.showinfo("Success", "Sale updated successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Error due to: {e}")

# Function to Delete Sale
def delete_sale():
    if id_var.get() == "":
        messagebox.showerror("Error", "Please select a sale to delete!")
    else:
        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM sales WHERE id=%s", (id_var.get(),))
            conn.commit()
            conn.close()
            fetch_sales()
            clear_fields()
            messagebox.showinfo("Success", "Sale deleted successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Error due to: {e}")

# Function to Clear Fields
def clear_fields():
    id_var.set("")
    product_id_var.set("")
    quantity_var.set("")
    total_price_var.set("")
    date_var.set("")

# Create Main Sales Window
sales_window = Tk()
sales_window.title("Sales Management")
sales_window.geometry("900x500")
sales_window.config(bg="LightGreen")
sales_window.attributes("-topmost", True)

# Title Label
title_label = Label(sales_window, text="Sales Management", font=("Arial", 20, "bold"), bg="DarkGreen", fg="white")
title_label.pack(side=TOP, fill=X)

# Variables
id_var = StringVar()
product_id_var = StringVar()
quantity_var = StringVar()
total_price_var = StringVar()
date_var = StringVar()

# Sales Form
form_frame = Frame(sales_window, bg="LightGreen")
form_frame.place(x=20, y=50, width=400, height=350)

Label(form_frame, text="Product ID:", font=("Arial", 12, "bold"), bg="LightGreen").grid(row=0, column=0, pady=10, sticky="w")
Entry(form_frame, textvariable=product_id_var, font=("Arial", 12)).grid(row=0, column=1, pady=10)

Label(form_frame, text="Quantity:", font=("Arial", 12, "bold"), bg="LightGreen").grid(row=1, column=0, pady=10, sticky="w")
Entry(form_frame, textvariable=quantity_var, font=("Arial", 12)).grid(row=1, column=1, pady=10)

Label(form_frame, text="Total Price:", font=("Arial", 12, "bold"), bg="LightGreen").grid(row=2, column=0, pady=10, sticky="w")
Entry(form_frame, textvariable=total_price_var, font=("Arial", 12)).grid(row=2, column=1, pady=10)

Label(form_frame, text="Sale Date:", font=("Arial", 12, "bold"), bg="LightGreen").grid(row=3, column=0, pady=10, sticky="w")
Entry(form_frame, textvariable=date_var, font=("Arial", 12)).grid(row=3, column=1, pady=10)

# Buttons
btn_frame = Frame(form_frame, bg="LightGreen")
btn_frame.grid(row=4, columnspan=2, pady=10)

Button(btn_frame, text="Add", font=("Arial", 12), bg="Green", fg="white", command=add_sale).grid(row=0, column=0, padx=5)
Button(btn_frame, text="Update", font=("Arial", 12), bg="Blue", fg="white", command=update_sale).grid(row=0, column=1, padx=5)
Button(btn_frame, text="Delete", font=("Arial", 12), bg="Red", fg="white", command=delete_sale).grid(row=0, column=2, padx=5)
Button(btn_frame, text="Clear", font=("Arial", 12), bg="Gray", fg="white", command=clear_fields).grid(row=0, column=3, padx=5)

# Sales Table
table_frame = Frame(sales_window)
table_frame.place(x=450, y=50, width=420, height=400)

columns = ("ID", "Product", "Quantity", "Total Price", "Sale Date")
sales_table = ttk.Treeview(table_frame, columns=columns, show="headings")
sales_table.column("ID", width=50)
sales_table.column("Product", width=120)
sales_table.column("Quantity", width=80)
sales_table.column("Total Price", width=100)
sales_table.column("Sale Date", width=100)
sales_table.heading("ID", text="ID")
sales_table.heading("Product", text="Product")
sales_table.heading("Quantity", text="Quantity")
sales_table.heading("Total Price", text="Total Price")
sales_table.heading("Sale Date", text="Sale Date")
sales_table.bind("<ButtonRelease-1>", select_sale)
sales_table.pack(fill=BOTH, expand=True)

# Fetch existing sales
fetch_sales()

# Run the Tkinter loop
sales_window.mainloop()
