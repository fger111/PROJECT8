import tkinter as tk
from tkinter import ttk
from pymongo import MongoClient
from ttkthemes import ThemedStyle
from tkinter import messagebox


# Connect to the MongoDB server
client = MongoClient('mongodb://localhost:27017/')
db = client['registration']

# Check if the user "Gastro-001" already exists in the database
user = db.users.find_one({'username': 'Gastro-001'})

# If the user "Gastro-001" doesn't exist, add them to the database
if not user:
    db.users.insert_one({'username': 'Gastro-001', 'password': 'gastroenterologist'})

def check_credentials():
    # Get the users from the input fields
    username = username_input.get()
    password = password_input.get()

    # Check if the username and password match any records
    user = db.users.find_one({'username': username, 'password': password})

    # If the username and password are correct
    if user:
        message_label.config(text="Login successful!", foreground="green")
        password_input.delete(0, tk.END)  # Clear the password entry field

        # Go to window module
        home_window()
    else:

        message_label.config(text="Wrong username or password", foreground="red")
        # Using grid layout
        message_label.grid(row=1, column=0, padx=915, pady=620)


def home_window():
    window.destroy()
    import home_window  # Import and run the searchbar module

# Create the main window
window = tk.Tk()
window.title("Log in Window")
window.geometry('700x600')
window.config(bg="#2c3e50")

# Configure the window to be full screen
window.state('zoomed')

# Create a themed style for the window
style = ThemedStyle(window)
style.set_theme("clam")

# Configure the colors
style.configure("TLabel", background="#2c3e50", foreground="#ffffff")
style.configure("TFrame", background="#2c3e50")
style.configure("TEntry", foreground="#2c3e50", background="#ffffff")
style.map("TButton", background=[('active', '#2c3e50')])

# Create the login frame
login_frame = ttk.Frame(window)
login_frame.pack(pady=100)

# Create the username input
username_label = ttk.Label(login_frame, text="Username:", font=("TkDefaultFont", 14))
username_label.grid(row=0, column=0, padx=10, pady=10)
username_input = ttk.Entry(login_frame)
username_input.grid(row=0, column=1, padx=10, pady=10)



# Create the password input
password_label = ttk.Label(login_frame, text="Password:", font=("TkDefaultFont", 14))
password_label.grid(row=1, column=0, padx=10, pady=10)
password_input = ttk.Entry(login_frame, show="*")
password_input.grid(row=1, column=1, padx=10, pady=10)




# Create the login button



style = ttk.Style()
style.configure("Custom.TButton", font=("TkDefaultFont", 14))

# Create the button with the custom style
login_button = ttk.Button(login_frame, text="Login", command=check_credentials, style="Custom.TButton")
login_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky='WE')



# Create the message
message_label = ttk.Label(window, text="", font=('Helvetica', 12))
message_label.pack()

# Center the login frame
login_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

# Run the application
window.mainloop()
