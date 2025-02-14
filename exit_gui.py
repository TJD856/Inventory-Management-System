from tkinter import *
from tkinter import messagebox
import sys

# Function to handle exit confirmation
def confirm_exit():
    """Ask for confirmation before exiting the application."""
    response = messagebox.askyesno("Exit Confirmation", "Are you sure you want to exit?")
    if response:
        sys.exit()  # Close the application

# Create Main Exit Window
exit_window = Tk()
exit_window.title("Exit Application")
exit_window.geometry("400x200")
exit_window.config(bg="LightCoral")
exit_window.attributes("-topmost", True)  # Ensure it stays on top

# Title Label
title_label = Label(exit_window, text="Confirm Exit", font=("Arial", 20, "bold"), bg="DarkRed", fg="white")
title_label.pack(side=TOP, fill=X)

# Exit Message
message_label = Label(exit_window, text="Do you really want to exit the application?", font=("Arial", 14), bg="LightCoral")
message_label.pack(pady=20)

# Buttons Frame
btn_frame = Frame(exit_window, bg="LightCoral")
btn_frame.pack()

# Yes and No Buttons
yes_button = Button(btn_frame, text="Yes", font=("Arial", 12), bg="Red", fg="white", width=10, command=confirm_exit)
yes_button.grid(row=0, column=0, padx=10)

no_button = Button(btn_frame, text="No", font=("Arial", 12), bg="Gray", fg="white", width=10, command=exit_window.destroy)
no_button.grid(row=0, column=1, padx=10)

# Run the Tkinter loop
exit_window.mainloop()
