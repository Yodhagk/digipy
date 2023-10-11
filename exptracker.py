import tkinter as tk
from tkinter import ttk
import mysql.connector as mysql
from tkinter import messagebox

# Function to save a record to the database
def save_record():
    date = date_entry.get()
    payee = payee_entry.get()
    description = description_entry.get()
    amount = amount_entry.get()
    mop = mop_entry.get()

    # Connect to the MySQL database (replace with your own database credentials)
    conn = mysql.connect(
        host="localhost",
        user="root",
        password="Citi@420",
        database="mydb"
    )
    cursor = conn.cursor()

    # Insert the record into the database
    insert_query = "INSERT INTO exptracker (date, payee, description, amount, mop) VALUES (%s, %s, %s, %s, %s)"
    values = (date, payee, description, amount, mop)

    try:
        cursor.execute(insert_query, values)
        conn.commit()
        messagebox.showinfo("Success", "Record saved successfully!")
        display_records()
    except mysql.Error as err:
        conn.rollback()
        messagebox.showerror("Error", f"Error: {err}")

    # Close the database connection
    conn.close()

# Function to display records from the database
def display_records():
    records_tree.delete(*records_tree.get_children())

    # Connect to the MySQL database (replace with your own database credentials)
    conn = mysql.connect(
        host="localhost",
        user="root",
        password="Citi@420",
        database="mydb"
    )
    cursor = conn.cursor()

    # Query the database for records
    cursor.execute("SELECT * FROM exptracker")
    records = cursor.fetchall()

    for record in records:
        records_tree.insert("", "end", values=record)

    # Close the database connection
    conn.close()

# Function to update a record
def update_record():
    selected_item = records_tree.selection()[0]
    record_id = records_tree.item(selected_item, 'values')[0]
    
    date = date_entry.get()
    payee = payee_entry.get()
    description = description_entry.get()
    amount = amount_entry.get()
    mop = mop_entry.get()
    
    # Connect to the MySQL database (replace with your own database credentials)
    conn = mysql.connect(
        host="localhost",
        user="root",
        password="Citi@420",
        database="mydb"
    )
    cursor = conn.cursor()
    
    # Update the record in the database
    update_query = "UPDATE exptracker SET date=%s, payee=%s, description=%s, amount=%s, mop=%s WHERE eid=%s"
    values = (date, payee, description, amount, mop, record_id)
    
    try:
        cursor.execute(update_query, values)
        conn.commit()
        messagebox.showinfo("Success", "Record updated successfully!")
        display_records()
    except mysql.Error as err:
        conn.rollback()
        messagebox.showerror("Error", f"Error: {err}")
    
    # Close the database connection
    conn.close()

# Function to delete a record
def delete_record():
    selected_item = records_tree.selection()[0]
    record_id = records_tree.item(selected_item, 'values')[0]
    
    # Connect to the MySQL database (replace with your own database credentials)
    conn = mysql.connect(
        host="localhost",
        user="root",
        password="Citi@420",
        database="mydb"
    )
    cursor = conn.cursor()
    
    # Delete the record from the database
    delete_query = "DELETE FROM exptracker WHERE eid=%s"
    value = (record_id,)
    
    try:
        cursor.execute(delete_query, value)
        conn.commit()
        messagebox.showinfo("Success", "Record deleted successfully!")
        display_records()
    except mysql.Error as err:
        conn.rollback()
        messagebox.showerror("Error", f"Error: {err}")
    
    # Close the database connection
    conn.close()

# Function to calculate the overall month amount spent
def calculate_monthly_total():
    selected_month = month_var.get()
    
    # Connect to the MySQL database (replace with your own database credentials)
    conn = mysql.connect(
        host="localhost",
        user="root",
        password="Citi@420",
        database="mydb"
    )
    cursor = conn.cursor()
    
    # Query the database to calculate the total amount for the selected month
    cursor.execute("SELECT SUM(amount) FROM exptracker WHERE DATE_FORMAT(date, '%Y-%m') = %s", (selected_month,))
    total_amount = cursor.fetchone()[0]
    
    # Close the database connection
    conn.close()
    
    # Display the total amount in the label
    total_label.config(text=f"Total Amount for {selected_month}: {total_amount or 0.0}")

# Create a GUI window for data entry and display
root = tk.Tk()
root.title("Expense Tracker")

# Create frames for left and right sections
left_frame = ttk.Frame(root)
left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

right_frame = ttk.Frame(root)
right_frame.grid(row=0, column=1, padx=10, pady=10, sticky="ne")

# Left Frame: Data Entry Form
ttk.Label(left_frame, text="Date (YYYY-MM-DD):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
date_entry = ttk.Entry(left_frame)
date_entry.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(left_frame, text="Payee:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
payee_entry = ttk.Entry(left_frame)
payee_entry.grid(row=1, column=1, padx=5, pady=5)

ttk.Label(left_frame, text="Description:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
description_entry = ttk.Entry(left_frame)
description_entry.grid(row=2, column=1, padx=5, pady=5)

ttk.Label(left_frame, text="Amount:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
amount_entry = ttk.Entry(left_frame)
amount_entry.grid(row=3, column=1, padx=5, pady=5)

ttk.Label(left_frame, text="MOP:").grid(row=4, column=0, padx=5, pady=5, sticky="w")
mop_entry = ttk.Entry(left_frame)
mop_entry.grid(row=4, column=1, padx=5, pady=5)

save_button = ttk.Button(left_frame, text="Save Record", command=save_record)
save_button.grid(row=5, column=0, columnspan=2, pady=10, padx=5, sticky="w")

update_button = ttk.Button(left_frame, text="Update Record", command=update_record)
update_button.grid(row=6, column=0, columnspan=2, pady=10, padx=5, sticky="w")

delete_button = ttk.Button(left_frame, text="Delete Record", command=delete_record)
delete_button.grid(row=7, column=0, columnspan=2, pady=10, padx=5, sticky="w")

# Right Frame: Data Viewing and Overall Monthly Amount
records_tree = ttk.Treeview(right_frame, columns=("ID", "Date", "Payee", "Description", "Amount", "MOP"), show="headings")
records_tree.heading("ID", text="ID")
records_tree.heading("Date", text="Date")
records_tree.heading("Payee", text="Payee")
records_tree.heading("Description", text="Description")
records_tree.heading("Amount", text="Amount")
records_tree.heading("MOP", text="MOP")

records_tree.pack()

# Month Selection Dropdown
ttk.Label(right_frame, text="Select Month:").pack()
month_var = tk.StringVar()
month_dropdown = ttk.Combobox(right_frame, textvariable=month_var)
month_dropdown['values'] = (
    "2023-01", "2023-02", "2023-03", "2023-04", "2023-05", "2023-06",
    "2023-07", "2023-08", "2023-09", "2023-10", "2023-11", "2023-12"
)
month_dropdown.pack()

calculate_button = ttk.Button(right_frame, text="Calculate Monthly Total", command=calculate_monthly_total)
calculate_button.pack()

# Label to display the overall monthly amount spent
total_label = ttk.Label(right_frame, text="")
total_label.pack()

# Display existing records
display_records()

root.mainloop()
