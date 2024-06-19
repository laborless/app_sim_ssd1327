import tkinter as tk
from PIL import Image, ImageTk, ImageDraw

# Constants
PIXEL_SIZE = 20 # 4
LINE_WIDTH = 1
X_RES = 10 # 128
Y_RES = 10 # 128

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
    # update_pixel_value(event.x, event.y)

# Function to update the displayed pixel value
# def update_pixel_value(x, y):
#     pixel_value = image.getpixel((x, y))
#     pixel_value_label.config(text=f"Pixel value: {pixel_value}")

def calc_canvas_size(x_res, y_res):
    width = x_res * PIXEL_SIZE + (x_res-1) * LINE_WIDTH
    height = y_res * PIXEL_SIZE + (y_res-1) * LINE_WIDTH

    return (width, height)

def update_canvas(canvas, x_res, y_res):
    c_width, c_height = calc_canvas_size(x_res, y_res)
    canvas.config(width=c_width, height=c_height)
    for line in range(PIXEL_SIZE, sz_canv[0], PIXEL_SIZE+LINE_WIDTH):
        canvas.create_line([(line, 0), (line, sz_canv[1])],fill='grey', tags='grid_line_w')
    for line in range(PIXEL_SIZE, sz_canv[1], PIXEL_SIZE+LINE_WIDTH):
        canvas.create_line([(0, line), (sz_canv[0], line)],fill='grey', tags='grid_line_h')

# Row0 - Menu & Buttons
btn_create = tk.Button(root, text="Create")
btn_create.grid(row=0, column=0)

btn_import = tk.Button(root, text="Import")
btn_import.grid(row=0, column=1)

btn_export = tk.Button(root, text="Export")
btn_export.grid(row=0, column=2)

btn_connect = tk.Button(root, text="Connect")
btn_connect.grid(row=0, column=4)
btn_disconnect = tk.Button(root, text="Disconnect")
btn_disconnect.grid(row=0, column=5)

# Row1 - Resolution X
lbl_res_x = tk.Label(root, text="res_x",)
lbl_res_x.grid(row=1, column=0)
etr_res_x = tk.Entry(root)
etr_res_x.insert("end", f"{X_RES}")
etr_res_x.grid(row=1, column=1)
# Row2 - Resolution Y
lbl_res_y = tk.Label(root, text="res_y")
lbl_res_y.grid(row=2, column=0)
etr_res_y = tk.Entry(root)
etr_res_y.insert("end", f"{Y_RES}")
etr_res_y.grid(row=2, column=1)

# Row3 - output
# Create a label to display pixel values
etr_output = tk.Entry(root)
etr_output.insert("end", "org:(0,0), grid:(0,0)")
etr_output.grid(row=3, column=0, columnspan=5)

# Row4 - canvas
# Create a canvas to draw on
sz_canv = calc_canvas_size(X_RES, Y_RES)
canvas = tk.Canvas(root, width=sz_canv[0], height=sz_canv[1], bg="white", 
                   highlightthickness=0, borderwidth=0) # remove border
for line in range(PIXEL_SIZE, sz_canv[0], PIXEL_SIZE+LINE_WIDTH):
    canvas.create_line([(line, 0), (line, sz_canv[1])],fill='grey', tags='grid_line_w')
for line in range(PIXEL_SIZE, sz_canv[1], PIXEL_SIZE+LINE_WIDTH):
    canvas.create_line([(0, line), (sz_canv[0], line)],fill='grey', tags='grid_line_h')
canvas.grid(row=4, column=0, columnspan=5)

# Bind mouse events to the canvas
canvas.bind("<B1-Motion>", paint)

# Row5 - log
etr_log = tk.Entry(root)
etr_log.insert("end", "hello log diablo is boring")
etr_log.grid(row=5, column=0, columnspan=5)

# Function to track mouse movement and update pixel value display
def motion(event):
    x_grid = event.x // (PIXEL_SIZE + LINE_WIDTH)
    y_grid = event.y // (PIXEL_SIZE + LINE_WIDTH)
    etr_output.delete("0", "end")
    etr_output.insert("end", f"org:({event.x},{event.y}), grid:({x_grid},{y_grid})")
    # pixel_value_label.config(text=f"org:({event.x},{event.y}), grid:({x_grid},{y_grid})")
    # x, y = event.x, event.y
    # if 0 <= x < 128 and 0 <= y < 128:
    #     update_pixel_value(x, y)

# Bind the motion event to the canvas
canvas.bind('<Motion>', motion)

# Run the Tkinter event loop
root.mainloop()
