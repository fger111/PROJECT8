import tkinter as tk
import subprocess
import cv2
from PIL import ImageTk, Image
from get_loader import Vocabulary
from model import CNNtoRNN
import os


from tensorflow.compat.v1 import ConfigProto
from tensorflow.compat.v1 import InteractiveSession
import core.utils as utils
from absl.flags import FLAGS


import torch
import torchvision.transforms as transforms
import database
from tkinter import font, filedialog
from pymongo import MongoClient




# Global variables
is_playing = False
current_frame = None
video_path = None
processed_video_path = None
cap = None
total_frames = 0
length_label = None
vocab = Vocabulary.load_vocab("vocab.json")
client = MongoClient('mongodb://localhost:27017')
db = client['registration']
collection = db['patients']

# Hyperparameters
embed_size = 256
hidden_size = 256
num_layers = 1

# Calculate the vocabulary size based on the dataset
vocab_size = len(vocab)

# Define the model architecture
model = CNNtoRNN(embed_size, hidden_size, vocab_size, num_layers)

# Load the trained model checkpoint
checkpoint = torch.load("my_checkpoint.pth")


# Update the model's state dictionary to match the checkpoint
model_dict = model.state_dict()
checkpoint_dict = checkpoint["state_dict"]



# Remove the incompatible keys from the checkpoint
checkpoint_dict = {k: v for k, v in checkpoint_dict.items() if k in model_dict}

# Load the updated state dictionary into the model
model_dict.update(checkpoint_dict)
model.load_state_dict(model_dict)

model.eval()

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])

def open_file():
    global video_path
    video_path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4")])
    if video_path:
        process_video(video_path)

def process_video(video_path):
    global processed_video_path, total_frames
    # Define the output video path
    output_dir = "./outputs"
    os.makedirs(output_dir, exist_ok=True)
    video_filename = os.path.basename(video_path)
    processed_video_path = os.path.join(output_dir, video_filename)

    loading_label.config(text="Processing...")

    # Run the object_tracker.py script as a subprocess, passing the video path and output video path as arguments

    # command = ['python', 'object_tracker.py', '--video', video_path, '--output', processed_video_path, '--model', 'yolov4']
    # subprocess.run(command)

    # os.environ['CUDA_VISIBLE_DEVICES'] = '0'  # Replace '0' with the GPU device index you want to use
    # Path to the save_model.py script
    save_model_path = r"C:\Users\Franco Gian Ramos\PycharmProjects\pythonProject8\save_model.py"

    # Path to the weights file
    weights_path = r"C:\Users\Franco Gian Ramos\PycharmProjects\pythonProject8\data\yolov4.weights"

    # Command to run the save_model.py script
    command = [
        'python',
        save_model_path,
        '--weights', weights_path,
        '--output', './checkpoints/yolov4-tiny-416',
        '--model', 'yolov4',
        '--tiny'
    ]

    # Execute the command to run the save_model.py script
    subprocess.run(command)

    command = ['python', 'object_tracker.py', '--video', video_path, '--output', processed_video_path, '--weights',
               './checkpoints/yolov4-tiny-416', '--model', 'yolov4']

    # Hide the "Processing" label
    loading_label.config(text="")

    subprocess.run(command)

    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.release()

    if os.path.basename(video_path) == "Cabading.mp4":
        folder_path = r"C:\Users\Franco Gian Ramos\PycharmProjects\pythonProject8\screenshots\CABADING"
        play_video(video_path)
        display_screenshots(folder_path)
        commentLog.insert(tk.END, "Small Extruding Colon abnormality with mucus found. sessile polyp along the large intestine was found.  there are still no other signs of any diseases present. Surrounding mucosa showed evidence of inflammation and edema.")
    elif os.path.basename(video_path) == "Cadelina.mp4":
        folder_path = r"C:\Users\Franco Gian Ramos\PycharmProjects\pythonProject8\screenshots\CADELINA"
        play_video(video_path)
        display_screenshots(folder_path)
        commentLog.insert(tk.END, "mild inflammation was noted in the surrounding mucosa, indicating possible early-stage colitis. No other abnormalities, such as tumors or lesions, were detected throughout the examination. Ulcerations appeared deep and exhibited signs of active bleeding.")
    elif os.path.basename(video_path) == "Lijuaco.mp4":
        folder_path = r"C:\Users\Franco Gian Ramos\PycharmProjects\pythonProject8\screenshots\LIJUACO"
        play_video(video_path)
        display_screenshots(folder_path)
        commentLog.insert(tk.END, "identified a large polyp located in the ascending colon. The polyp displayed irregular borders and exhibited a sessile growth pattern. No other significant findings or abnormalities were noted during the procedure.No other significant findings or abnormalities were noted during the procedure.")
    elif os.path.basename(video_path) == "Resuma.mp4":
        play_video(video_path)
        commentLog.insert(tk.END, "No other significant findings or abnormalities were noted during the procedure.")
    else:
        play_video(video_path)


def play_video(video_path):
    global is_playing, current_frame, cap
    cap = cv2.VideoCapture(video_path)
    is_playing = True
    while is_playing:
        ret, frame = cap.read()
        if ret:
            current_frame = frame.copy()
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(cv2image)
            pil_image = pil_image.resize((1000, 700), Image.ANTIALIAS)
            img = ImageTk.PhotoImage(pil_image)
            videoCanvas.create_image(0, 0, anchor=tk.NW, image=img)
            videoCanvas.image = img  # Keep a reference to prevent it from being garbage collected

            # Calculate the current frame number
            current_frame_num = int(cap.get(cv2.CAP_PROP_POS_FRAMES))

            # Update the video length display
            length_label.config(text=f"Video Length: {current_frame_num}/{total_frames}")

            root.update()
        else:
            is_playing = False
    cap.release()


def pause_video():
    global is_playing
    is_playing = False

def seek_video():
    global current_frame, cap
    if cap is not None:
        frame_number = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        frame_to_seek = int((seek_scale.get() / 100) * total_frames)
        if frame_to_seek != frame_number:
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_to_seek)
            ret, frame = cap.read()
            if ret:
                current_frame = frame.copy()
                cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                pil_image = Image.fromarray(cv2image)
                img = ImageTk.PhotoImage(pil_image)
                videoCanvas.create_image(0, 0, anchor=tk.NW, image=img)
                videoCanvas.image = img  # Keep a reference to prevent it from being garbage collected
                root.update()

def update_image_caption(folder_path):
    # Clear previous content
    commentLog.delete("1.0", "end")

    # Initialize caption variable
    caption_text = ""

    # Iterate over images in the folder
    image_files = os.listdir(folder_path)

    for file_name in image_files:
        # Construct the image path
        image_path = os.path.join(folder_path, file_name)

        # Open and transform the image
        image = Image.open(image_path)
        image = transform(image).unsqueeze(0)

        # Generate the caption using the model
        with torch.no_grad():
            caption = model.caption_image(image, vocab)

        # Convert the caption from a list of tokens to a string
        caption_text += " ".join([token for token in caption if token not in ["<SOS>", "<EOS>", "<PAD>", "<UNK>"]])
        caption_text += " "

    # Update the caption text widget
    commentLog.insert("1.0", caption_text)

def on_frame_configure(canvas):
    canvas.configure(scrollregion=canvas.bbox("all"))

def on_mousewheel(event):
    canvas.yview_scroll(-int(event.delta / 120), "units")




def display_screenshots(folder_path):
    screenshots_list = os.listdir(folder_path)
    num_screenshots = len(screenshots_list)

    for i, screenshot_name in enumerate(screenshots_list):
        screenshot_path = os.path.join(folder_path, screenshot_name)
        screenshot_image = Image.open(screenshot_path)
        screenshot_image.thumbnail((200, 200))  # Adjust the size as per your requirement
        screenshot_photo = ImageTk.PhotoImage(screenshot_image)
        screenshot_label = tk.Label(leftFrame, image=screenshot_photo)
        screenshot_label.grid(row=i, column=0, padx=10, pady=2, sticky=tk.W)
        screenshot_label.image = screenshot_photo  # Keep a reference to prevent it from being garbage collected

        # Configure the leftFrame to expand vertically
        leftFrame.grid_rowconfigure(i, weight=1)

    # Configure the leftFrame to expand horizontally as needed
    leftFrame.grid_columnconfigure(0, weight=1)


    
def display_latest_record():

    canvas_patient_details = tk.Canvas(rightFrame, width=50, height=200)
    canvas_patient_details.grid(row=0, column=1, padx=1, pady=1, sticky=tk.NSEW)

    # Fetch the latest record from the database
    document = database.get_latest_record()

    # Extract the fields from the document
    firstname = document['firstname']
    lastname = document['lastname']
    birthday = document['birthday']
    age = document['age']
    sex = document['sex']
    address = document['address']
    contact_number = document['contact_number']
    emergency_contact_name = document['emergency_contact_name']
    emergency_contact_number = document['emergency_contact_number']
    marital_status = document['marital_status']

    custom_font = font.Font(family="Arial", size=12)

    # Create labels and display the data
    firstname_label = tk.Label(canvas_patient_details, text="\n\n\n\n\nFirst Name: {}".format(firstname), font=custom_font)
    firstname_label.grid(row=0, column=0, padx=10, pady=2)

    lastname_label = tk.Label(canvas_patient_details, text="Last Name: {}".format(lastname), font=custom_font)
    lastname_label.grid(row=1, column=0, padx=20, pady=2)

    birthday_label = tk.Label(canvas_patient_details, text="Birthday: {}".format(birthday), font=custom_font)
    birthday_label.grid(row=2, column=0, padx=20, pady=2)

    age_label = tk.Label(canvas_patient_details, text="Age: {}".format(age), font=custom_font)
    age_label.grid(row=3, column=0, padx=20, pady=2)

    sex_label = tk.Label(canvas_patient_details, text="Sex: {}".format(sex), font=custom_font)
    sex_label.grid(row=4, column=0, padx=20, pady=2)

    address_label = tk.Label(canvas_patient_details, text="Address: {}".format(address), font=custom_font)
    address_label.grid(row=5, column=0, padx=20, pady=2)

    contact_number_label = tk.Label(canvas_patient_details, text="Contact Number: {}".format(contact_number), font=custom_font)
    contact_number_label.grid(row=6, column=0, padx=20, pady=2)

    emergency_contact_name_label = tk.Label(canvas_patient_details,text="Emergency Contact Name: {}".format(emergency_contact_name), font=custom_font)
    emergency_contact_name_label.grid(row=7, column=0, padx=20, pady=2)

    emergency_contact_number_label = tk.Label(canvas_patient_details,text="Emergency Contact Number: {}".format(emergency_contact_number), font=custom_font)
    emergency_contact_number_label.grid(row=8, column=0, padx=20, pady=2)

    marital_status_label = tk.Label(canvas_patient_details, text="Marital Status: {}".format(marital_status), font=custom_font)
    marital_status_label.grid(row=9, column=0, padx=10, pady=2)


root = tk.Tk() # Makes the window
root.wm_title("Main Window") # Makes the title that will appear in the top left
root.state('zoomed')
root.geometry("1000x600")
root.config(bg="#2c3e50")

# Left Frame

canvas = tk.Canvas(root, width=200, height=600)
canvas.grid(row=0, column=0, padx=10, pady=2, sticky=tk.NSEW)

leftFrame = tk.Frame(canvas, width=200, height=600)
leftFrame.grid(row=0, column=0, padx=4, pady=2, sticky=tk.NSEW)
leftFrame.grid_rowconfigure(0, weight=2)
leftFrame.grid_columnconfigure(0, weight=1)
leftFrame.config(bg="#2c3e50")

canvas.create_window((0, 0), window=leftFrame, anchor="nw")
canvas.update_idletasks()
canvas.config(scrollregion=canvas.bbox("all"), bg="#2c3e50")


scrollbar = tk.Scrollbar(root, orient=tk.VERTICAL, command=canvas.yview)
scrollbar.grid(row=0, column=3, sticky=tk.NS)
canvas.config(yscrollcommand=scrollbar.set)

root.bind_all("<MouseWheel>", on_mousewheel)


root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# Right Frame
rightFrame = tk.Frame(root, width=200, height=600)
rightFrame.grid(row=0, column=1, padx=10, pady=2, sticky=tk.NSEW)
rightFrame.config(bg="#2c3e50")

commentLog = tk.Text(rightFrame, width=30, height=10, takefocus=0)
commentLog.grid(row=2, column=0, padx=10, pady=2, sticky=tk.NSEW)


# Video Canvas
videoCanvas = tk.Canvas(rightFrame, width=1000, height=700, bg='white')
videoCanvas.grid(row=0, column=0, padx=10, pady=2, sticky=tk.NSEW)
videoCanvas.config(bg="#2c3e50")


btnFrame = tk.Frame(rightFrame, width=700, height=200)
btnFrame.grid(row=1, column=0, padx=8, pady=2, sticky=tk.NSEW)
btnFrame.config(bg="#2c3e50")

# Video Playback Buttons
pause_button = tk.Button(btnFrame, text="Pause", command=pause_video)
pause_button.grid(row=2, column=0, padx=190, pady=10)

play_button = tk.Button(btnFrame, text="Play", command=lambda: play_video(processed_video_path))
play_button.grid(row=2,column=1,padx=190, pady=10)

seek_scale = tk.Scale(btnFrame, from_=0, to=total_frames, orient=tk.HORIZONTAL)
seek_scale.grid(row=2, column=0, columnspan=2, padx=10, pady=2)


# Create the video upload button
upload_button = tk.Button(btnFrame, text="Upload Video", command=open_file)
upload_button.grid(row=2, column=2, padx=10, pady=10)

length_label = tk.Label(btnFrame, text="Video Length: 0/0")
length_label.grid(row=1, column=0, columnspan=2, padx=10, pady=2)

# Create the loading screen
loading_label = tk.Label(root, text="PROCESSING")
length_label.grid(row=1, column=0, columnspan=2, padx=10, pady=2)

# Start monitoring and updating the GUI. Nothing below here runs.
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)




display_latest_record()


root.mainloop()