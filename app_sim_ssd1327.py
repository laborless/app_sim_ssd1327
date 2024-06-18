import tkinter as tk
from tkinter import colorchooser

class PaintApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Paint App")

        # Set up the canvas
        self.canvas = tk.Canvas(self.root, bg='white', width=128, height=128)
        self.canvas.pack()

        # Initialize color and brush size
        self.brush_color = 'black'
        self.brush_size = 5

        # Bind mouse events to canvas
        self.canvas.bind('<B1-Motion>', self.paint)
        self.canvas.bind('<ButtonRelease-1>', self.reset)

        # Create color picker button
        self.color_button = tk.Button(self.root, text='Pick Color', command=self.choose_color)
        self.color_button.pack(side='left')

        # Create brush size buttons
        self.brush_size_frame = tk.Frame(self.root)
        self.brush_size_frame.pack(side='left', fill='both', expand=True)
        self.size_label = tk.Label(self.brush_size_frame, text='Brush Size:')
        self.size_label.pack(side='left')
        self.size_slider = tk.Scale(self.brush_size_frame, from_=1, to=10, orient='horizontal')
        self.size_slider.set(self.brush_size)
        self.size_slider.pack(side='left')

    def paint(self, event):
        # Get brush size and color
        brush_size = self.size_slider.get()
        color = self.brush_color
        
        # Draw an oval (dot) where the mouse is
        x1, y1 = (event.x - brush_size), (event.y - brush_size)
        x2, y2 = (event.x + brush_size), (event.y + brush_size)
        self.canvas.create_oval(x1, y1, x2, y2, fill=color, outline=color)

    def reset(self, event):
        # Reset the last_drawn variable
        self.last_drawn = None

    def choose_color(self):
        # Open color chooser and set new brush color
        self.brush_color = colorchooser.askcolor(color=self.brush_color)[1]

if __name__ == '__main__':
    root = tk.Tk()
    app = PaintApp(root)
    root.mainloop()
