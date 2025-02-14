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

# Function to Add Product
def add_product():
    if name_var.get() == "" or price_var.get() == "" or stock_var.get() == "" or category_var.get() == "":
        messagebox.showerror("Error", "All fields are required!")
    else:
        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO products (name, category_id, price, stock) VALUES (%s, %s, %s, %s)",
                           (name_var.get(), category_var.get(), price_var.get(), stock_var.get()))
            conn.commit()
            conn.close()
            fetch_products()
            clear_fields()
            messagebox.showinfo("Success", "Product added successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Error due to: {e}")

# Function to Fetch Products
def fetch_products():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT p.id, p.name, c.name, p.price, p.stock FROM products p INNER JOIN categories c ON p.category_id = c.id")
    rows = cursor.fetchall()
    product_table.delete(*product_table.get_children())
    for row in rows:
        product_table.insert("", END, values=row)
    conn.close()

# Function to Select Product from Table
def select_product(event):
    selected_row = product_table.focus()
    content = product_table.item(selected_row)
    row = content["values"]
    if row:
        id_var.set(row[0])
        name_var.set(row[1])
        category_var.set(row[2])
        price_var.set(row[3])
        stock_var.set(row[4])

# Function to Update Product
def update_product():
    if id_var.get() == "":
        messagebox.showerror("Error", "Please select a product to update!")
    else:
        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("UPDATE products SET name=%s, category_id=%s, price=%s, stock=%s WHERE id=%s",
                           (name_var.get(), category_var.get(), price_var.get(), stock_var.get(), id_var.get()))
            conn.commit()
            conn.close()
            fetch_products()
            clear_fields()
            messagebox.showinfo("Success", "Product updated successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Error due to: {e}")

# Function to Delete Product
def delete_product():
    if id_var.get() == "":
        messagebox.showerror("Error", "Please select a product to delete!")
    else:
        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM products WHERE id=%s", (id_var.get(),))
            conn.commit()
            conn.close()
            fetch_products()
            clear_fields()
            messagebox.showinfo("Success", "Product deleted successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Error due to: {e}")

# Function to Clear Fields
def clear_fields():
    id_var.set("")
    name_var.set("")
    category_var.set("")
    price_var.set("")
    stock_var.set("")

# Create Main Product Window
product_window = Tk()
product_window.title("Product Management")
product_window.geometry("900x500")
product_window.config(bg="LightBlue")
product_window.attributes("-topmost", True)

# Title Label
title_label = Label(product_window, text="Product Management", font=("Arial", 20, "bold"), bg="DarkBlue", fg="white")
title_label.pack(side=TOP, fill=X)

# Variables
id_var = StringVar()
name_var = StringVar()
category_var = StringVar()
price_var = StringVar()
stock_var = StringVar()

# Product Form
form_frame = Frame(product_window, bg="LightBlue")
form_frame.place(x=20, y=50, width=400, height=350)

Label(form_frame, text="Product Name:", font=("Arial", 12, "bold"), bg="LightBlue").grid(row=0, column=0, pady=10, sticky="w")
Entry(form_frame, textvariable=name_var, font=("Arial", 12)).grid(row=0, column=1, pady=10)

Label(form_frame, text="Category ID:", font=("Arial", 12, "bold"), bg="LightBlue").grid(row=1, column=0, pady=10, sticky="w")
Entry(form_frame, textvariable=category_var, font=("Arial", 12)).grid(row=1, column=1, pady=10)

Label(form_frame, text="Price:", font=("Arial", 12, "bold"), bg="LightBlue").grid(row=2, column=0, pady=10, sticky="w")
Entry(form_frame, textvariable=price_var, font=("Arial", 12)).grid(row=2, column=1, pady=10)

Label(form_frame, text="Stock:", font=("Arial", 12, "bold"), bg="LightBlue").grid(row=3, column=0, pady=10, sticky="w")
Entry(form_frame, textvariable=stock_var, font=("Arial", 12)).grid(row=3, column=1, pady=10)

# Buttons
btn_frame = Frame(form_frame, bg="LightBlue")
btn_frame.grid(row=4, columnspan=2, pady=10)

Button(btn_frame, text="Add", font=("Arial", 12), bg="Green", fg="white", command=add_product).grid(row=0, column=0, padx=5)
Button(btn_frame, text="Update", font=("Arial", 12), bg="Blue", fg="white", command=update_product).grid(row=0, column=1, padx=5)
Button(btn_frame, text="Delete", font=("Arial", 12), bg="Red", fg="white", command=delete_product).grid(row=0, column=2, padx=5)
Button(btn_frame, text="Clear", font=("Arial", 12), bg="Gray", fg="white", command=clear_fields).grid(row=0, column=3, padx=5)

# Product Table
table_frame = Frame(product_window)
table_frame.place(x=450, y=50, width=420, height=400)

columns = ("ID", "Name", "Category", "Price", "Stock")
product_table = ttk.Treeview(table_frame, columns=columns, show="headings")
product_table.column("ID", width=50)
product_table.column("Name", width=120)
product_table.column("Category", width=100)
product_table.column("Price", width=80)
product_table.column("Stock", width=80)
product_table.heading("ID", text="ID")
product_table.heading("Name", text="Name")
product_table.heading("Category", text="Category")
product_table.heading("Price", text="Price")
product_table.heading("Stock", text="Stock")
product_table.bind("<ButtonRelease-1>", select_product)
product_table.pack(fill=BOTH, expand=True)

# Fetch existing products
fetch_products()

# Run the Tkinter loop
product_window.mainloop()
