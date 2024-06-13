import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
from tkinter import filedialog
import subprocess
import cv2
import csv

def select_file():
    file_path = filedialog.askopenfilename(title="Select an image or video file", filetypes=[("Image files", "*.jpg;*.png;*.jpeg"), ("Video files", "*.mp4")])
    if file_path:
        entry_file.delete(0, tk.END)
        entry_file.insert(0, file_path)
        display_thumbnail(file_path)

def run_detection():
    file_path = entry_file.get()
    if file_path:
        # Run detect.py
        subprocess.run(['python', r'E:/Final projects/smart-traffic-monitor-main/smart-traffic-monitor-main/yolo/detect.py', '--weights',  r'E:\Final projects\smart-traffic-monitor-main\smart-traffic-monitor-main\yolo\runs\train\exp\weights\best.pt', '--source', file_path, '--save-crop'])
        # Run main.py
        subprocess.run(['python', 'main.py'])
       
def display_thumbnail(file_path):
    global thumbnail_canvas
    thumbnail_canvas.delete("all")
    if file_path.lower().endswith(('.png', '.jpg', '.jpeg')):
        # Display image thumbnail
        image = Image.open(file_path)
        image.thumbnail((250, 250))  # Resize image if it's too large
        photo = ImageTk.PhotoImage(image)
        thumbnail_canvas.create_image(0, 0, anchor="nw", image=photo)
        thumbnail_canvas.image = photo  # Keep a reference to avoid garbage collection
    elif file_path.lower().endswith('.mp4'):
        # Display video thumbnail
        cap = cv2.VideoCapture(file_path)
        ret, frame = cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (250, 250))
            image = Image.fromarray(frame)
            photo = ImageTk.PhotoImage(image=image)
            thumbnail_canvas.create_image(0, 0, anchor="nw", image=photo)
            thumbnail_canvas.image = photo  # Keep a reference to avoid garbage collection
        cap.release()

def display_database():
    # Clear existing table data
    for row in tree.get_children():
        tree.delete(row)
    
    # Read data from the CSV file and populate the table
    with open('database.csv', 'r') as file:
        reader = csv.reader(file)
        for idx, row in enumerate(reader):
            if idx == 0:  # Skip header row
                continue
            tree.insert('', 'end', values=row)

# Create the main window
root = tk.Tk()
root.title("Traffic Violation Monitoring System")

# Function to resize and set background image
def resize_bg(event):
    # Resize the image to match the window size
    bg_image_resized = bg_image.resize((event.width, event.height), Image.ANTIALIAS)
    bg_photo = ImageTk.PhotoImage(bg_image_resized)
    canvas.create_image(0, 0, image=bg_photo, anchor="nw")
    canvas.image = bg_photo  # Keep a reference to avoid garbage collection

# Loading the background image
bg_image = Image.open("background.jpeg")  # Provide the path to your background image

# Creating a Canvas to place the background image
canvas = tk.Canvas(root)
canvas.pack(fill="both", expand=True)  # Fill the entire window
canvas.bind("<Configure>", resize_bg)  # Bind to window resize events

# Header
header_label = tk.Label(root, text="Traffic Violation Monitoring System", font=("Helvetica", 50, "bold"))
header_label.place(relx=0.5, rely=0.1, anchor="center")

# Frame to hold the image selection elements
frame_file = tk.Frame(root)
frame_file.place(relx=0.5, rely=0.2, anchor="center")
label_file = tk.Label(frame_file, text="Select an image or video file:", font=("Helvetica", 12))
label_file.pack(side=tk.LEFT)
entry_file = tk.Entry(frame_file, width=50, font=("Helvetica", 12))
entry_file.pack(side=tk.LEFT, padx=10)
button_browse = tk.Button(frame_file, text="Browse", command=select_file, font=("Helvetica", 12))
button_browse.pack(side=tk.LEFT)

# Thumbnail Canvas
thumbnail_canvas = tk.Canvas(root, bg="white", width=250, height=250)
thumbnail_canvas.place(relx=0.5, rely=0.5, anchor="center")

# Database Table
tree_frame = tk.Frame(root)
tree_frame.place(relx=0.5, rely=0.75, anchor="center")
tree = ttk.Treeview(tree_frame, columns=(1, 2, 3, 4, 5), show="headings", height="5")
tree.pack(side=tk.LEFT)
tree.heading(1, text="Name")
tree.heading(2, text="Registration")
tree.heading(3, text="Phone number")
tree.heading(4, text="Email")
tree.heading(5, text="Due challan")
display_database()  # Populate the table with data from database.csv

# Run Detection Button
button_run_detection = tk.Button(root, text="Run Detection", command=run_detection, font=("Helvetica", 14, "bold"), bg="green", fg="white")
button_run_detection.place(relx=0.5, rely=0.9, anchor="center")

# Footer
footer_label = tk.Label(root, text="© 2024 Helmet Detection Inc.", font=("Helvetica", 16))
footer_label.place(relx=0.5, rely=0.95, anchor="center")

# Run the Tkinter event loop
root.mainloop()
