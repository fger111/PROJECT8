import tkinter as tk

def register_patient():
    window.destroy()  # Close the main window
    import register_window

def search_patient():
    window.destroy()  # Close the main window
    import searchbar_window
    
# Create the main window
window = tk.Tk()
window.title("DEEP-COLON")
window.geometry('700x500')
window.config(bg="#2c3e50")

window.state('zoomed')

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x = (screen_width // 2) - (600 // 2)
y = (screen_height // 2) - (600 // 2)
window.geometry(f'+{x}+{y}')

# Create and configure the labels and buttons
title_label = tk.Label(window, text="Welcome to DEEP-COLON", font=("Helvetica", 24, "bold"), fg="#ffffff", bg="#2c3e50")
title_label.place(relx=0.5, rely=0.2, anchor="center")

register_button = tk.Button(window, text="Register Patient", font=("Arial", 16), width=20, height=3, command=register_patient, bg="#3498db", fg="#ffffff")
register_button.place(relx=0.3, rely=0.5, anchor="center")

search_button = tk.Button(window, text="Search Patient", font=("Arial", 16), width=20, height=3, command=search_patient, bg="#2980b9", fg="#ffffff")
search_button.place(relx=0.7, rely=0.5, anchor="center")

window.grid_columnconfigure(0, weight=1)
window.grid_columnconfigure(1, weight=1)
window.grid_columnconfigure(2, weight=1)

# Start the main event loop
window.mainloop()
