from tkinter import *

# Initialize the main window
window = Tk()

# Configure the window properties
window.title('Dashboard')
window.geometry('1350x700+0+0')
window.config(bg='Lavender')

# Ensure the window stays on top of other applications
window.attributes("-topmost", True)

# Background image
bg_image = PhotoImage(file=r'C:\Users\jagad\OneDrive\Documents\Desktop\PYJD\inventory\inventory.png')
titleLabel = Label(window, image=bg_image, compound=LEFT, text='  \tInventory Management System ',
                   font=('times new roman', 40, 'bold'), bg='#010c48', fg='white', anchor='w', padx=20)
titleLabel.place(x=0, y=0, relwidth=1)

# Logout Button
logoutButton = Button(window, text='Logout', font=('times new roman', 20, 'bold'), fg='#010c48')
logoutButton.place(x=1100, y=10)

# Subtitle Label
subtitleLabel = Label(window, text='Welcome Admin\t\t  Date: 02-02-2025\t\t  Time:5:27:17 pm',
                      font=('times new roman', 15), bg='#4d636d', fg='white')
subtitleLabel.place(x=0, y=70, relwidth=1)

# Left frame for the menu
leftFrame = Frame(window)
leftFrame.place(x=0, y=102, width=200, height=555)

suppyimage = PhotoImage(file=r'C:\Users\jagad\OneDrive\Documents\Desktop\PYJD\inventory\supply-chain.png')
imageLabel = Label(leftFrame, image=suppyimage)
imageLabel.pack()

menuLabel = Label(leftFrame, text='Menu', font=('times new roman', 20), bg='#009688')
menuLabel.pack(fill=X)

# Menu Buttons
Employee_button = Button(leftFrame, text='Employees', font=('times new roman', 20, 'bold'), anchor='w', padx=10)
Employee_button.pack(fill=X)

Supplier_button = Button(leftFrame, text='Suppliers', font=('times new roman', 20, 'bold'), anchor='w', padx=10)
Supplier_button.pack(fill=X)

Category_button = Button(leftFrame, text='Categories', font=('times new roman', 20, 'bold'), anchor='w', padx=10)
Category_button.pack(fill=X)

Products_button = Button(leftFrame, text='Products', font=('times new roman', 20, 'bold'), anchor='w', padx=10)
Products_button.pack(fill=X)

Sales_button = Button(leftFrame, text='Sales', font=('times new roman', 20, 'bold'), anchor='w', padx=10)
Sales_button.pack(fill=X)

Exit_button = Button(leftFrame, text='Exit', font=('times new roman', 20, 'bold'), anchor='w', padx=10)
Exit_button.pack(fill=X)

# Frames for statistics
emp_Frame = Frame(window, bg='#2C3E50', bd=3, relief=RIDGE)
emp_Frame.place(x=400, y=125, height=170, width=280)

Label(emp_Frame, text='Total Employees', bg='#2C3E50', fg='white', font=('times new roman', 15, 'bold')).pack()
Label(emp_Frame, text='200', bg='#2C3E50', fg='white', font=('times new roman', 30, 'bold')).pack()

supplier_Frame = Frame(window, bg='#2C3E50', bd=3, relief=RIDGE)
supplier_Frame.place(x=800, y=125, height=170, width=280)

Label(supplier_Frame, text='Total Suppliers', bg='#2C3E50', fg='white', font=('times new roman', 15, 'bold')).pack()
Label(supplier_Frame, text='10', bg='#2C3E50', fg='white', font=('times new roman', 30, 'bold')).pack()

cat_Frame = Frame(window, bg='#2C3E50', bd=3, relief=RIDGE)
cat_Frame.place(x=400, y=310, height=170, width=280)

Label(cat_Frame, text='Total Categories', bg='#2C3E50', fg='white', font=('times new roman', 15, 'bold')).pack()
Label(cat_Frame, text='10', bg='#2C3E50', fg='white', font=('times new roman', 30, 'bold')).pack()

pro_Frame = Frame(window, bg='#2C3E50', bd=3, relief=RIDGE)
pro_Frame.place(x=800, y=310, height=170, width=280)

Label(pro_Frame, text='Total Products', bg='#2C3E50', fg='white', font=('times new roman', 15, 'bold')).pack()
Label(pro_Frame, text='10', bg='#2C3E50', fg='white', font=('times new roman', 30, 'bold')).pack()

sal_Frame = Frame(window, bg='#2C3E50', bd=3, relief=RIDGE)
sal_Frame.place(x=600, y=495, height=170, width=280)

Label(sal_Frame, text='Total Sales', bg='#2C3E50', fg='white', font=('times new roman', 15, 'bold')).pack()
Label(sal_Frame, text='80', bg='#2C3E50', fg='white', font=('times new roman', 30, 'bold')).pack()

# Run the Tkinter loop
window.mainloop()