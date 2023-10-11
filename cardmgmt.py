import tkinter as tk
from tkinter import ttk
import mysql.connector

# Connect to your MySQL database (replace with your own database configuration)
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Citi@420",
    database="mydb"
)

cursor = db.cursor()

def save_record():
    bname = bname_entry.get()
    cnumber = cnumber_entry.get()
    emonth = emonth_entry.get()
    eyear = eyear_entry.get()
    cvv = cvv_entry.get()
    status = status_entry.get()
    
    sql = "INSERT INTO ccards (bname, cnumber, emonth, eyear, cvv, status) VALUES (%s, %s, %s, %s, %s, %s)"
    values = (bname, cnumber, emonth, eyear, cvv, status)
    
    cursor.execute(sql, values)
    db.commit()
    
    clear_entries()
    display_records()

def clear_entries():
    bname_entry.delete(0, tk.END)
    cnumber_entry.delete(0, tk.END)
    emonth_entry.delete(0, tk.END)
    eyear_entry.delete(0, tk.END)
    cvv_entry.delete(0, tk.END)
    status_entry.delete(0, tk.END)

def display_records():
    records_tree.delete(*records_tree.get_children())
    cursor.execute("SELECT * FROM ccards")
    records = cursor.fetchall()
    
    for record in records:
        records_tree.insert("", "end", values=record)

def update_record():
    selected_item = records_tree.selection()[0]
    record_id = records_tree.item(selected_item, 'values')[0]
    status = status_entry.get()
    
    cursor.execute("UPDATE ccards SET status=%s WHERE card_id=%s", (status, record_id))
    db.commit()
    
    display_records()

def delete_record():
    selected_item = records_tree.selection()[0]
    record_id = records_tree.item(selected_item, 'values')[0]
    
    cursor.execute("DELETE FROM ccards WHERE card_id=%s", (record_id,))
    db.commit()
    
    display_records()

# Create the main window
root = tk.Tk()
root.title("Credit Card Management")

# Create and place form elements
frame = ttk.Frame(root)
frame.grid(row=0, column=0, padx=10, pady=10)

ttk.Label(frame, text="Card Holder Name:").grid(row=0, column=0, sticky="w")
bname_entry = ttk.Entry(frame)
bname_entry.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(frame, text="Card Number:").grid(row=1, column=0, sticky="w")
cnumber_entry = ttk.Entry(frame)
cnumber_entry.grid(row=1, column=1, padx=5, pady=5)

ttk.Label(frame, text="Expiry Month:").grid(row=2, column=0, sticky="w")
emonth_entry = ttk.Entry(frame)
emonth_entry.grid(row=2, column=1, padx=5, pady=5)

ttk.Label(frame, text="Expiry Year:").grid(row=3, column=0, sticky="w")
eyear_entry = ttk.Entry(frame)
eyear_entry.grid(row=3, column=1, padx=5, pady=5)

ttk.Label(frame, text="CVV:").grid(row=4, column=0, sticky="w")
cvv_entry = ttk.Entry(frame)
cvv_entry.grid(row=4, column=1, padx=5, pady=5)

ttk.Label(frame, text="Status:").grid(row=5, column=0, sticky="w")
status_entry = ttk.Entry(frame)
status_entry.grid(row=5, column=1, padx=5, pady=5)

save_button = ttk.Button(frame, text="Save Record", command=save_record)
save_button.grid(row=6, column=0, columnspan=2, pady=10)

# Create and place a treeview widget for displaying records
records_tree = ttk.Treeview(root, columns=("ID", "Card Holder", "Card Number", "Expiry Month", "Expiry Year", "CVV", "Status"), show="headings")
records_tree.heading("ID", text="ID")
records_tree.heading("Card Holder", text="Card Holder")
records_tree.heading("Card Number", text="Card Number")
records_tree.heading("Expiry Month", text="Expiry Month")
records_tree.heading("Expiry Year", text="Expiry Year")
records_tree.heading("CVV", text="CVV")
records_tree.heading("Status", text="Status")

records_tree.grid(row=1, column=0, padx=10, pady=10)

display_records()

update_button = ttk.Button(root, text="Update Record", command=update_record)
update_button.grid(row=2, column=0, padx=10, pady=5)

delete_button = ttk.Button(root, text="Delete Record", command=delete_record)
delete_button.grid(row=2, column=1, padx=10, pady=5)

root.mainloop()

# Close the database connection when the application exits
db.close()
