import tkinter as tk
from PIL import Image, ImageTk, ImageDraw

# Initialize the main application window
root = tk.Tk()
root.title("Python Paint App")

# Create a 128x128 white image
image = Image.new("RGB", (128, 128), "white")
image_draw = ImageDraw.Draw(image)

# Function to update the image when drawing
def paint(event):
    x1, y1 = (event.x - 1), (event.y - 1)
    x2, y2 = (event.x + 1), (event.y + 1)
    image_draw.ellipse([x1, y1, x2, y2], fill="black", outline="black")
    canvas.create_oval(x1, y1, x2, y2, fill="black", outline="black")
    update_pixel_value(event.x, event.y)

# Function to update the displayed pixel value
def update_pixel_value(x, y):
    pixel_value = image.getpixel((x, y))
    pixel_value_label.config(text=f"Pixel value: {pixel_value}")

# Create a canvas to draw on
canvas = tk.Canvas(root, width=128, height=128, bg="white")
canvas.pack(side=tk.BOTTOM)

# Bind mouse events to the canvas
canvas.bind("<B1-Motion>", paint)

# Create a label to display pixel values
pixel_value_label = tk.Label(root, text="Pixel value: (0, 0, 0)")
pixel_value_label.pack(side=tk.TOP)

# Function to track mouse movement and update pixel value display
def motion(event):
    x, y = event.x, event.y
    if 0 <= x < 128 and 0 <= y < 128:
        update_pixel_value(x, y)

# Bind the motion event to the canvas
canvas.bind('<Motion>', motion)

# Run the Tkinter event loop
root.mainloop()
