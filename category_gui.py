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

# Function to Add Category
def add_category():
    if name_var.get() == "":
        messagebox.showerror("Error", "Category name is required!")
    else:
        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO categories (name, description) VALUES (%s, %s)",
                           (name_var.get(), desc_var.get()))
            conn.commit()
            conn.close()
            fetch_categories()
            clear_fields()
            messagebox.showinfo("Success", "Category added successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Error due to: {e}")

# Function to Fetch Categories
def fetch_categories():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM categories")
    rows = cursor.fetchall()
    category_table.delete(*category_table.get_children())
    for row in rows:
        category_table.insert("", END, values=row)
    conn.close()

# Function to Select Category from Table
def select_category(event):
    selected_row = category_table.focus()
    content = category_table.item(selected_row)
    row = content["values"]
    if row:
        id_var.set(row[0])
        name_var.set(row[1])
        desc_var.set(row[2])

# Function to Update Category
def update_category():
    if id_var.get() == "":
        messagebox.showerror("Error", "Please select a category to update!")
    else:
        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("UPDATE categories SET name=%s, description=%s WHERE id=%s",
                           (name_var.get(), desc_var.get(), id_var.get()))
            conn.commit()
            conn.close()
            fetch_categories()
            clear_fields()
            messagebox.showinfo("Success", "Category updated successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Error due to: {e}")

# Function to Delete Category
def delete_category():
    if id_var.get() == "":
        messagebox.showerror("Error", "Please select a category to delete!")
    else:
        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM categories WHERE id=%s", (id_var.get(),))
            conn.commit()
            conn.close()
            fetch_categories()
            clear_fields()
            messagebox.showinfo("Success", "Category deleted successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Error due to: {e}")

# Function to Clear Fields
def clear_fields():
    id_var.set("")
    name_var.set("")
    desc_var.set("")

# Create Main Category Window
category_window = Tk()
category_window.title("Category Management")
category_window.geometry("800x500")
category_window.config(bg="LightGreen")
category_window.attributes("-topmost", True)

# Title Label
title_label = Label(category_window, text="Category Management", font=("Arial", 20, "bold"), bg="DarkGreen", fg="white")
title_label.pack(side=TOP, fill=X)

# Variables
id_var = StringVar()
name_var = StringVar()
desc_var = StringVar()

# Category Form
form_frame = Frame(category_window, bg="LightGreen")
form_frame.place(x=20, y=50, width=350, height=300)

Label(form_frame, text="Category Name:", font=("Arial", 12, "bold"), bg="LightGreen").grid(row=0, column=0, pady=10, sticky="w")
Entry(form_frame, textvariable=name_var, font=("Arial", 12)).grid(row=0, column=1, pady=10)

Label(form_frame, text="Description:", font=("Arial", 12, "bold"), bg="LightGreen").grid(row=1, column=0, pady=10, sticky="w")
Entry(form_frame, textvariable=desc_var, font=("Arial", 12)).grid(row=1, column=1, pady=10)

# Buttons
btn_frame = Frame(form_frame, bg="LightGreen")
btn_frame.grid(row=2, columnspan=2, pady=10)

Button(btn_frame, text="Add", font=("Arial", 12), bg="Green", fg="white", command=add_category).grid(row=0, column=0, padx=5)
Button(btn_frame, text="Update", font=("Arial", 12), bg="Blue", fg="white", command=update_category).grid(row=0, column=1, padx=5)
Button(btn_frame, text="Delete", font=("Arial", 12), bg="Red", fg="white", command=delete_category).grid(row=0, column=2, padx=5)
Button(btn_frame, text="Clear", font=("Arial", 12), bg="Gray", fg="white", command=clear_fields).grid(row=0, column=3, padx=5)

# Category Table
table_frame = Frame(category_window)
table_frame.place(x=400, y=50, width=380, height=400)

columns = ("ID", "Name", "Description")
category_table = ttk.Treeview(table_frame, columns=columns, show="headings")
category_table.column("ID", width=50)
category_table.column("Name", width=150)
category_table.column("Description", width=150)
category_table.heading("ID", text="ID")
category_table.heading("Name", text="Name")
category_table.heading("Description", text="Description")
category_table.bind("<ButtonRelease-1>", select_category)
category_table.pack(fill=BOTH, expand=True)

# Fetch existing categories
fetch_categories()

# Run the Tkinter loop
category_window.mainloop()
