import tkinter as tk
from PIL import ImageTk
from tkinter import PhotoImage


def start_button_clicked():
    window.destroy()  # Close the main window
    import home_window

window = tk.Tk()
window.title("DEEP-COLON")
window.geometry('380x150')
window.config(bg="gray")
window.resizable(False,False)

image = PhotoImage(file="deep- (1).png")
label = tk.Label(window, image=image)
label.grid(row=0, column=0, padx=110, pady=20, columnspan=3, sticky="nesw")



start_button = tk.Button(window, text="Start", font=("Georgia", 8), width=10, height=3, command=start_button_clicked)
start_button.grid(row=2, column=0, padx=150, pady=10, sticky="nesw")


window.mainloop()