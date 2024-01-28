import tkinter as tk
from PIL import Image, ImageTk
from datetime import datetime
import time
import math
from queue import Queue

def show_label(text):
    label.config(text=text)
    root.update()

def show_face():
    show_label("Show the face")

def enter_fingerprint():
    show_label("Enter the fingerprint")

def enter_key():
    show_label("Enter the key")

def world():
    label.config(text="World")
    root.update()

def go():
    label.config(text="goooo")
    root.update()

def randnum():
    random_value = random.randint(2, 6)
    time.sleep(random_value)

def update_time():
    current_time = time.strftime("%H:%M:%S")
    draw_clock_hands()
    root.after(1000, update_time)

def update_date():
    current_date = datetime.now().strftime("%Y-%m-%d %A")
    date_label.config(text=current_date)
    root.after(60000, update_date)

def draw_clock_hands():
    now = datetime.now()
    seconds = now.second
    minutes = now.minute
    hours = now.hour % 12  

    # Clear previous drawings
    canvas.delete("all")

    # Draw clock face
    canvas.create_oval(10, 10, 190, 190, width=4, outline="#3498db", fill="#ecf0f1")

    # Draw numbers
    for i in range(1, 13):
        angle = math.radians(90 - 30 * i)
        x = 100 + 80 * math.cos(angle)
        y = 100 - 80 * math.sin(angle)
        canvas.create_text(x, y, text=str(i), font=("Helvetica", 10), fill="#2c3e50")

    # Draw hour hand
    hour_angle = math.radians(-(30 * (hours - 3) + 0.5 * minutes))
    hour_x = 100 + 40 * math.cos(hour_angle)
    hour_y = 100 - 40 * math.sin(hour_angle)
    canvas.create_line(100, 100, hour_x, hour_y, width=4, fill="#2c3e50")

    # Draw minute hand
    minute_angle = math.radians(-(6 * (minutes - 15) + 0.1 * seconds))
    minute_x = 100 + 60 * math.cos(minute_angle)
    minute_y = 100 - 60 * math.sin(minute_angle)
    canvas.create_line(100, 100, minute_x, minute_y, width=2, fill="#2c3e50")
   
    # Draw second hand
    second_angle = math.radians(-(6 * (seconds - 15)))
    second_x = 100 + 70 * math.cos(second_angle)
    second_y = 100 - 70 * math.sin(second_angle)
    canvas.create_line(100, 100, second_x, second_y, width=1, fill="#e74c3c")

def run_gui(queue):
    global root, canvas, label, date_label
    root = tk.Tk()
    root.geometry("800x480")

    # Load and resize the background image
    background_image = Image.open("background.jpg").resize((800, 480))
    background_photo = ImageTk.PhotoImage(background_image)

    # Create a label for the background image
    background_label = tk.Label(root, image=background_photo)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Create a canvas for drawing the clock face with enhanced styling
    canvas = tk.Canvas(root, width=200, height=200, bg='lightgray', borderwidth=2, relief="solid")
    canvas.place(relx=0.33, rely=0.7, anchor='center')  # Center the canvas in the window

    # Add a circle representing the clock face
    canvas.create_oval(5, 5, 195, 195, outline='black', width=2)

    # Add smaller hour markers
    for i in range(12):
        angle = i * (360 / 12)
        x1 = 100 + 80 * math.cos(math.radians(angle))
        y1 = 100 - 80 * math.sin(math.radians(angle))
        x2 = 100 + 90 * math.cos(math.radians(angle))
        y2 = 100 - 90 * math.sin(math.radians(angle))
        canvas.create_line(x1, y1, x2, y2, width=2)

    # Add a smaller center point
    canvas.create_oval(97, 97, 103, 103, fill='black')

    # Create a label for displaying the date
    date_label = tk.Label(
        root,
        text="January 22, 2024",
        font=("Arial", 18, "italic"),
        fg='green',  # Set foreground color
        bg='lightyellow',  # Set background color
        padx=10,  # Add padding on the x-axis
        pady=5,  # Add padding on the y-axis
        borderwidth=2,  # Add a border
        relief="solid",  # Specify border style
        width=15,  # Set a fixed width
    )

    # Place the date label to the right side of the window
    date_label.pack(pady=10, anchor='e')
    date_label.place(relx=0.7, rely=0.7, anchor='center')

    # Create a label for displaying messages
    label = tk.Label(
        root,
        text="Welcome to Face Secure!",
        font=("Arial", 36, "bold italic"),
        fg='blue',  # Set foreground color
        bg='lightgray',  # Set background color
        padx=20,  # Add padding on the x-axis
        pady=10,  # Add padding on the y-axis
        borderwidth=5,  # Add a border
        relief="solid",  # Specify border style
        width=30,  # Set a fixed width
    )

    # Place the label in the center of the window
    label.pack(pady=50)
    label.place(relx=0.5, rely=0.2, anchor='center')

    # Call the example function
    update_time()
    update_date()

    while True:
        if not queue.empty():
            message = queue.get()
            show_label(message)
        root.update()
        time.sleep(0.1)  # Adjust as needed

    # Start the Tkinter event loop
    root.mainloop()
