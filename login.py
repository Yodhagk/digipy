import mysql.connector
import tkinter as tk
from tkinter import messagebox

# Function to handle the login button click
def login():
    username = entry_username.get()
    password = entry_password.get()

    # Connect to the MySQL database
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Citi@420",
        database="mydb"
    )
    cursor = conn.cursor()

    # Query the database to check if the user exists
    cursor.execute("SELECT userid, safekey FROM users WHERE userid = %s AND safekey = %s", (username, password))
    user = cursor.fetchone()

    if user:
        messagebox.showinfo("Login Successful", "Welcome, User ID: {}".format(user[0]))
    else:
        messagebox.showerror("Login Failed", "Invalid User ID or Safekey")

    # Close the database connection
    conn.close()

# Create a GUI window
root = tk.Tk()
root.title("Expense Tracker Login")
root.geometry('400x300')

# Create labels, entry widgets, and login button
label_username = tk.Label(root, text="User ID:")  # Corrected to use 'tk.Label'
label_password = tk.Label(root, text="Safekey:")  # Corrected to use 'tk.Label'
entry_username = tk.Entry(root)
entry_password = tk.Entry(root, show="*")  # Use 'show' to hide the password characters
button_login = tk.Button(root, text="Login", command=login)  # Corrected to use 'tk.Button'

# Place widgets on the window
label_username.grid(row=0, column=0)
entry_username.grid(row=0, column=1)
label_password.grid(row=1, column=0)
entry_password.grid(row=1, column=1)
button_login.grid(row=2, columnspan=2)  # Use 'grid' instead of 'pack'

# Start the GUI main loop
root.mainloop()
