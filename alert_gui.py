import tkinter as tk
from tkinter import messagebox, ttk
import pandas as pd

# Sample dataset for testing
data = [
    {'Item ID': 1, 'Name': 'Pen', 'Category': 'Stationery', 'Quantity': 5, 'Price': 10},
    {'Item ID': 2, 'Name': 'Notebook', 'Category': 'Stationery', 'Quantity': 12, 'Price': 50},
    {'Item ID': 3, 'Name': 'Mouse', 'Category': 'Electronics', 'Quantity': 8, 'Price': 500},
    {'Item ID': 4, 'Name': 'Keyboard', 'Category': 'Electronics', 'Quantity': 15, 'Price': 800}
]
df = pd.DataFrame(data)

# GUI Setup
root = tk.Tk()
root.title("Inventory Management System")
root.geometry("600x400")

# Treeview for inventory display
tree = ttk.Treeview(root, columns=("ID", "Name", "Category", "Quantity", "Price"), show='headings')
columns = ["ID", "Name", "Category", "Quantity", "Price"]
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=100)
tree.pack(fill=tk.BOTH, expand=True)

# Function to populate data
def load_data():
    for row in df.itertuples():
        tree.insert("", "end", values=(row._1, row.Name, row.Category, row.Quantity, row.Price))
        if row.Quantity <= 10:
            messagebox.showwarning("Low Stock Alert", f"{row.Name} is running low on stock ({row.Quantity} left)")

# Load data into the table
load_data()

# Run GUI
root.mainloop()
