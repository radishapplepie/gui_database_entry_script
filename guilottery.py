#This script creates a gui environment to enter information about scratch off lottery tickets, then upload them into a database file with
#sqlite3 in order to later be able to take an overhead look at your percentages.
#cost is the cost of the ticket. (int in db)
#name is the name of the ticket. (str in db)
#win amount is the amount the ticket is worth after scratching. (int, and 0 means complete loser obviously)
#misc is misc information. (str, info like wildcard prozes, or anything else)

import sqlite3
import tkinter as tk
from tkinter import messagebox

database_file = "<your_db_file.db>"

int_cost = None
name_input = None
int_win = None
misc_input = None

#funtion to inssert new entry to sqlite3 database
def insert_ticket(db_name, ticket_data):
	conn = None
	try:
		conn = sqlite3.connect(db_name)
		cursor = conn.cursor()
		
		sql_query = """
		INSERT INTO testtable (cost, name, win_amt, misc)
		VALUES (?, ?, ?, ?);
		"""
        	
		cursor.execute(sql_query, ticket_data)
        	
		conn.commit()
		print("Ticket data added successfuly")
        	
	except sqlite3.Error as e:
		print(f"Error occurred: {e}")
	
	finally:
		if conn:
			conn.close()

#set the cost on button or enter			
def on_cost_enter(event = None):
	global int_cost
	cost_input = cost_entry.get()
	try:
		int_cost = int(cost_input)
		cost_entry.delete(0, tk.END)
		cost_label.config(text=f"Cost entered: {int_cost}")
		print(f"Cost entered: {int_cost} (type: {type(int_cost)})")
	except ValueError:
		messagebox.showerror("Invalid Input", "Please enter a valid integer for the cost.")
		cost_entry.delete(0, tk.END)

#set the name on button or enter
def on_name_enter(event = None):
	global name_input
	name_input = name_entry.get()
	name_entry.delete(0, tk.END)
	name_to_display = f"Name entered: {name_input}"
	name_label.config(text=name_to_display)
	print(name_input)

#set the win(or likely lose) amount on button or enter
def on_win_enter(event = None):
	global int_win
	win_input = win_amt_entry.get()
	try:
		int_win = int(win_input)
		win_amt_entry.delete(0, tk.END)
		win_label.config(text=f"Win amount entered: {int_win}")
		print(f"Win amount entered: {int_win} (type: {type(int_win)})")
	except ValueError:
		messagebox.showerror("Invalid Input", "Please enter a valid integer for the win amount.")
		win_amt_entry.delete(0, tk.END)

#set the misc on button or enter
def on_misc_enter(event = None):
	global misc_input
	misc_input = misc_entry.get()
	misc_entry.delete(0, tk.END)
	misc_to_display = f"Misc entered: {misc_input}"
	misc_label.config(text=misc_to_display)
	print(misc_input)

#this function checks that everything is in place correctly and then adds the sqlite3 entry into the table in the database
def on_db_entry():
	global int_cost, name_input, int_win, misc_input
	if int_cost is None or name_input is None or int_win is None or misc_input is None:
		messagebox.showerror("Incomplete Data", "Please submit all entries before clicking DB Entry.")
	else:
		ticket_entry = (int_cost, name_input, int_win, misc_input)
		print(ticket_entry)
		insert_ticket(database_file, ticket_entry)
		success_label.config(text=f"Submitted successfully: {ticket_entry}")
		db_radio_var.set(0)
		toggle_db_button()

#radio button that is there to act as one more confimation that all the user input data is correct
def toggle_db_button():
    if db_radio_var.get() == 1:
        db_button.config(state=tk.NORMAL)
    else:
        db_button.config(state=tk.DISABLED)
	
def bexit():
	window.destroy()
			
#main gui window			
window = tk.Tk()
window.title("Scratch ticket entries")

# Add a centered title label at the top
title_label = tk.Label(window, text="Scratch Ticket Entry", font=("Helvetica", 16, "bold"))
title_label.pack(pady=10)

# Use a single main frame for all inputs to keep them organized
main_frame = tk.Frame(window)
main_frame.pack(pady=10, padx=10)

# New frame for the radio button and DB Entry button
db_frame = tk.Frame(window)
db_frame.pack(pady=10)

# Create an IntVar to track the radio button's state
db_radio_var = tk.IntVar()

#Frame where you'll be told whether the sql add is successful or not
success_label = tk.Label(window, text="")
success_label.pack(pady=2)

#Label to display output once each category is submitted to show what is held in the variable. can be changed contnuously
cost_label = tk.Label(window, text="")
cost_label.pack(pady=1)

name_label = tk.Label(window, text="")
name_label.pack(pady=1)

win_label = tk.Label(window, text="")
win_label.pack(pady=1)

misc_label = tk.Label(window, text="")
misc_label.pack(pady=1)

#frame for exit button
exit_button_frame = tk.Frame(window)
exit_button_frame.pack(pady = 2)

# We use grid to place labels and entries in a table-like format
# Column 0 is for the labels, and Column 1 is for the entry boxes

# Row 0: Cost
cost_entry_label = tk.Label(main_frame, text="Cost:")
cost_entry_label.grid(row=0, column=0, sticky=tk.E, padx=5, pady=5)
cost_entry = tk.Entry(main_frame, width=10)
cost_entry.grid(row=0, column=1, padx=5, pady=5)
cost_entry.bind("<Return>", on_cost_enter)

cost_button = tk.Button(main_frame, text="Submit", command=on_cost_enter)
cost_button.grid(row=0, column=2, padx=5, pady=5)

# Row 1: Name
name_entry_label = tk.Label(main_frame, text="Name:")
name_entry_label.grid(row=1, column=0, sticky=tk.E, padx=5, pady=5)
name_entry = tk.Entry(main_frame, width=10)
name_entry.grid(row=1, column=1, padx=5, pady=5)
name_entry.bind("<Return>", on_name_enter)

name_button = tk.Button(main_frame, text="Submit", command=on_name_enter)
name_button.grid(row=1, column=2, padx=5, pady=5)

# Row 2: Amount won
win_amt_entry_label = tk.Label(main_frame, text="Amount won:")
win_amt_entry_label.grid(row=2, column=0, sticky=tk.E, padx=5, pady=5)
win_amt_entry = tk.Entry(main_frame, width=10)
win_amt_entry.grid(row=2, column=1, padx=5, pady=5)
win_amt_entry.bind("<Return>", on_win_enter)

win_button = tk.Button(main_frame, text="Submit", command=on_win_enter)
win_button.grid(row=2, column=2, padx=5, pady=5)

# Row 3: Misc
misc_entry_label = tk.Label(main_frame, text="Misc:")
misc_entry_label.grid(row=3, column=0, sticky=tk.E, padx=5, pady=5)
misc_entry = tk.Entry(main_frame, width=10)
misc_entry.grid(row=3, column=1, padx=5, pady=5)
misc_entry.bind("<Return>", on_misc_enter)

misc_button = tk.Button(main_frame, text="Submit", command=on_misc_enter)
misc_button.grid(row=3, column=2, padx=5, pady=5)

# Create the radio button and the DB Entry button
db_radio_button = tk.Radiobutton(db_frame, text="Ready", variable=db_radio_var, value=1, command=toggle_db_button)
db_radio_button.pack(side=tk.LEFT)

db_button = tk.Button(db_frame, text="DB Entry", state=tk.DISABLED, command=on_db_entry)
db_button.pack(side=tk.LEFT, padx=10)

exit = tk.Button(exit_button_frame, text = "Exit", command = bexit)
exit.pack(pady = 2)

window.mainloop()
