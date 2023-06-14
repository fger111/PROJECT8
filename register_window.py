import tkinter as tk
import tkcalendar
from tkinter import ttk
from tkinter import messagebox
from pymongo import MongoClient
import database
from tkinter import filedialog
import os



# Connect to the MongoDB server
client = MongoClient("mongodb://localhost:27017/")

# Access the database and create a collection if it doesn't exist
db = client["registration"]
collection = db["patients"]





def save_video_data():
    global video_path
    if video_path:
        print("Video Path:", video_path)  # Debug: Check the video path
        with open(video_path, 'rb') as file:
            # Read the video file as binary data
            video_data = file.read()
            print("Video Data Size:", len(video_data))  # Debug: Check the size of video_data

    return video_data

def enter_data():
        global video_path
        # Personal info
        firstname = firstname_entry.get()
        lastname = lastname_entry.get()
        birthday = birthday_entry.get()
        age = age_entry.get()
        sex = sex_combobox.get()

        # Contact info
        address = address_entry.get()
        contact_number = contact_number_entry.get()
        emergency_contact_name = emergency_contact_name_entry.get()
        emergency_contact_number = emergency_contact_number_entry.get()
        marital_status = marital_status_combobox.get()

        if firstname and lastname and birthday and age and sex and address and contact_number and emergency_contact_name and emergency_contact_number and marital_status:
            # Insert data into the collection
            database.insert_data(firstname, lastname, birthday, age, sex, address, contact_number, emergency_contact_name, emergency_contact_number, marital_status)

            # Display success message
            messagebox.showinfo(title="Success", message="Data entered successfully!")

            window.destroy()
            import view


        else:
            # Display error message if any field is blank
            messagebox.showerror(title="Error", message="Please fill up all fields.")

window = tk.Tk()
window.title("Data Entry Form")
window.geometry('700x600')
window.config(bg="#2c3e50")

window.state('zoomed')

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x = (screen_width // 2) - (600 // 2)
y = (screen_height // 2) - (600 // 2)
window.geometry(f'+{x}+{y}')

def back_home():
    window.withdraw()
    window.destroy()
    import home_window

button_style = ttk.Style()
button_style.configure("Custom.TButton", font=("Arial", 32))

frame = tk.Frame(window, bg="#2c3e50")
frame.pack(padx=10, pady=10, fill="both", expand=True)

# Personal Information Frame
personal_info_frame = tk.LabelFrame(frame, text="Personal Information", bg="#2c3e50", fg="#ffffff", font=("Arial", 32, "bold"))
personal_info_frame.pack(padx=10, pady=10, fill="both", expand=True)


firstname_label = tk.Label(personal_info_frame, text="First Name:", font=("Arial", 32), bg="#2c3e50", fg="#ffffff")
firstname_label.grid(row=0, column=0, sticky="e", padx=10, pady=10)
firstname_entry = tk.Entry(personal_info_frame, width=50, font=("Arial", 32))
firstname_entry.grid(row=0, column=1, padx=10, pady=10)

lastname_label = tk.Label(personal_info_frame, text="Last Name:", font=("Arial", 32), bg="#2c3e50", fg="#ffffff")
lastname_label.grid(row=1, column=0, sticky="e", padx=10, pady=10)
lastname_entry = tk.Entry(personal_info_frame, width=50, font=("Arial", 32))
lastname_entry.grid(row=1, column=1, padx=10, pady=10)

age_label = tk.Label(personal_info_frame, text="Age:", font=("Arial", 32), bg="#2c3e50", fg="#ffffff")
age_label.grid(row=2, column=0, sticky="e", padx=10, pady=10)
age_entry = tk.Entry(personal_info_frame, width=50, font=("Arial", 32))
age_entry.grid(row=2, column=1, padx=10, pady=10)

sex_label = tk.Label(personal_info_frame, text="Sex:", font=("Arial", 32), bg="#2c3e50", fg="#ffffff")
sex_label.grid(row=3, column=0, sticky="e", padx=10, pady=10)

sex_combobox = ttk.Combobox(personal_info_frame, values=["Male", "Female"], font=("Arial", 32), width=49)
sex_combobox.grid(row=3, column=1, padx=10, pady=10)

birthday_label = tk.Label(personal_info_frame, text="Birthday:", font=("Arial", 32), bg="#2c3e50", fg="#ffffff")
birthday_label.grid(row=4, column=0, sticky="e", padx=10, pady=10)
birthday_entry = tkcalendar.DateEntry(personal_info_frame, date_pattern='yyyy-mm-dd', width=49, font=("Arial", 32))
birthday_entry.grid(row=4, column=1, padx=10, pady=10)


# Contact Information Frame
contact_info_frame = tk.LabelFrame(frame, text="Contact Information", bg="#2c3e50", fg="#ffffff", font=("Arial", 32, "bold"))
contact_info_frame.pack(padx=10, pady=10, fill="both", expand=True)

address_label = tk.Label(contact_info_frame, text="Address:", font=("Arial", 32), bg="#2c3e50", fg="#ffffff")
address_label.grid(row=0, column=0, sticky="e", padx=10, pady=10)
address_entry = tk.Entry(contact_info_frame, width=50, font=("Arial", 32))
address_entry.grid(row=0, column=1, padx=10, pady=10)

contact_number_label = tk.Label(contact_info_frame, text="Contact Number:", font=("Arial", 32), bg="#2c3e50", fg="#ffffff")
contact_number_label.grid(row=1, column=0, sticky="e", padx=10, pady=10)
contact_number_entry = tk.Entry(contact_info_frame, width=50, font=("Arial", 32))
contact_number_entry.grid(row=1, column=1, padx=10, pady=10)

emergency_contact_name_label = tk.Label(contact_info_frame, text="Emergency Contact Name:", font=("Arial", 32), bg="#2c3e50", fg="#ffffff")
emergency_contact_name_label.grid(row=2, column=0, sticky="e", padx=10, pady=10)
emergency_contact_name_entry = tk.Entry(contact_info_frame, width=50, font=("Arial", 32))
emergency_contact_name_entry.grid(row=2, column=1, padx=10, pady=10)

emergency_contact_number_label = tk.Label(contact_info_frame, text="Emergency Contact Number:", font=("Arial", 32), bg="#2c3e50", fg="#ffffff")
emergency_contact_number_label.grid(row=3, column=0, sticky="e", padx=10, pady=10)
emergency_contact_number_entry = tk.Entry(contact_info_frame, width=50, font=("Arial", 32))
emergency_contact_number_entry.grid(row=3, column=1, padx=10, pady=10)

marital_status_label = tk.Label(contact_info_frame, text="Marital Status:", font=("Arial", 32), bg="#2c3e50", fg="#ffffff")
marital_status_label.grid(row=6, column=0, sticky="e", padx=10, pady=10)

marital_status_combobox = ttk.Combobox(contact_info_frame, values=["Single", "Married", "Divorced", "Widowed"], font=("Arial", 32))
marital_status_combobox.grid(row=6, column=1, padx=10, pady=10, sticky="ew", columnspan=2)

# Submit Button
submit_button = ttk.Button(frame, text="Submit", command=enter_data, style="Custom.TButton")
submit_button.pack(side="right", padx=10, pady=10)

# Back button
back_button = ttk.Button(frame, text="Back", command=back_home, style="Custom.TButton")
back_button.pack(side="bottom", padx=10, pady=10, anchor="w")








window.mainloop()
