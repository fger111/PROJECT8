import tkinter as tk
from tkinter import ttk
from pymongo import MongoClient

# Define function to handle name click event
def show_user_details(event):
    # Get the selected item from the listbox
    selected_item = search_results.get(search_results.curselection())

    # Extract the name from the selected item
    name = selected_item.split("Name: ")[1].split(" Birthday:")[0]

    # Create a new window to display user details
    details_window = tk.Toplevel(window)
    details_window.title('User Details')
    details_window.geometry('400x200')

    # Retrieve and display user details
    client = MongoClient('mongodb://localhost:27017/')
    db = client["registration"]
    collection = db["patients"]

    user_data = collection.find_one({"firstname": name.split()[0], "lastname": name.split()[1]})

    if user_data:
        details_label = ttk.Label(details_window, text=f"User Details\n\nName: {user_data['firstname']} {user_data['lastname']}\nBirthday: {user_data['birthday']}\nAge: {user_data['age']}\nSex: {user_data['sex']}\nAddress: {user_data['address']}\nContact Number: {user_data['contact_number']}\nEmergency Contact Number: {user_data['emergency_contact_number']}\nEmergency Contact Name: {user_data['emergency_contact_name']}\nMarital Status: {user_data['marital_status']}", font=('Arial', 12))
        details_label.pack(pady=10)
    else:
        details_label = ttk.Label(details_window, text="User details not found.", font=('Arial', 12))
        details_label.pack(pady=10)

    client.close()

    # Close the current window after showing the user details
    window.destroy()
    import view

# Define function to handle search button click
def search_users():
    # Clear any previous search results
    search_results.delete(0, tk.END)

    # Get search term from input box
    search_term = search_input.get()

    # Connect to MongoDB and perform search
    client = MongoClient('mongodb://localhost:27017/')
    db = client["registration"]
    collection = db["patients"]

    results = collection.find({"lastname": {"$regex": search_term, "$options": "i"}})

    if len(list(results)) > 0:
        # Display search results
        results.rewind()  # Rewind the cursor back to the beginning
        for result in results:
            search_results.insert(tk.END, f"Name: {result['firstname']} {result['lastname']}  Birthday: {result['birthday']}   Age: {result['age']}   Sex: {result['sex']}   Address: {result['address']}   Contact Number: {result['contact_number']}  Emergency Contact Number: {result['emergency_contact_number']}  Emergency Contact Name: {result['emergency_contact_name']} Marital Status: {result['marital_status']}")
    else:
        # Display message if no results found
        search_results.insert(tk.END, "No results found.")

    client.close()

# Create GUI window
window = tk.Tk()
window.title('User Search')
window.geometry('700x500')
window.config(bg="#2c3e50")  # Navy blue background color

window.state('zoomed')

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x = (screen_width - window.winfo_reqwidth()) // 2
y = (screen_height - window.winfo_reqheight()) // 2

window.geometry(f'+{x}+{y}')

# Define styles
style = ttk.Style(window)
style.theme_use('clam')
style.configure('TLabel', font=('Arial', 12), foreground="#000000")
style.configure('TEntry', font=('Arial', 12))
style.configure('TButton', font=('Arial', 12), foreground="#000000", background="#2980b9")

# Add search elements
search_label = ttk.Label(window, text='Search for user by last name:', foreground="#000000")
search_label.pack(pady=10)

search_input = ttk.Entry(window, width=30)
search_input.pack()

search_button = ttk.Button(window, text='Search', command=search_users, style='TButton', width=15)
search_button.pack(pady=10)

search_results = tk.Listbox(window, width=100, height=30, font=('Arial', 12))
search_results.pack()

# Bind listbox click event to show_user_details function
search_results.bind('<<ListboxSelect>>', show_user_details)

window.grid_columnconfigure(0, weight=1)
window.grid_columnconfigure(1, weight=1)
window.grid_columnconfigure(2, weight=1)

# Start GUI loop
window.mainloop()
