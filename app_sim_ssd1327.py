import tkinter as tk
from PIL import Image, ImageTk, ImageDraw

# Constants
PIXEL_SIZE = 25 # 4
LINE_WIDTH = 1
X_RES = 20 # 128
Y_RES = 20 # 128

# Initialize the main application window
root = tk.Tk()
root.title("Python Paint App")

# Create a 128x128 white image (8bit grey scale)
image = Image.new("L", (X_RES, Y_RES), "white")
image_draw = ImageDraw.Draw(image)

# Function to update the image when drawing
def paint(event):
    # to do brush color
    x_grid = event.x // (PIXEL_SIZE + LINE_WIDTH)
    y_grid = event.y // (PIXEL_SIZE + LINE_WIDTH)
    image_draw.point([(x_grid, y_grid)], fill="black")


    x_st = x_grid * (PIXEL_SIZE + LINE_WIDTH)
    y_st = y_grid * (PIXEL_SIZE + LINE_WIDTH)
    canvas.create_rectangle(x_st, y_st, x_st + PIXEL_SIZE, y_st + PIXEL_SIZE, fill="black", width=0)

    pixel_value = image.getpixel((x_grid, y_grid))
    colour = "black" if pixel_value > 128 else "white"
    canvas.create_text(x_st+PIXEL_SIZE//2, y_st+PIXEL_SIZE//2, text = f"{hex(pixel_value//16)}", fill=colour, font=(f'Helvetica {PIXEL_SIZE//3}'))
    
    update_pixel_value(x_grid, y_grid)

# Function to update the displayed pixel value
def update_pixel_value(x, y):
    pixel_value = image.getpixel((x, y))
    pixel_value_label.config(text=f"Pixel value: {pixel_value}")

def calc_canvas_size(x_res, y_res):
    width = x_res * PIXEL_SIZE + (x_res-1) * LINE_WIDTH
    height = y_res * PIXEL_SIZE + (y_res-1) * LINE_WIDTH

    return (width, height)

def update_canvas(canvas, x_res, y_res):
    c_width, c_height = calc_canvas_size(x_res, y_res)
    canvas.config(width=c_width, height=c_height)
    # draw_grid
    for line in range(PIXEL_SIZE, c_width, PIXEL_SIZE+LINE_WIDTH):
        canvas.create_line([(line, 0), (line, c_height)],fill='grey', tags='grid_line_w')
    for line in range(PIXEL_SIZE, c_height, PIXEL_SIZE+LINE_WIDTH):
        canvas.create_line([(0, line), (c_width, line)],fill='grey', tags='grid_line_h')
    # draw colour
    for pos_x in range(PIXEL_SIZE//2, c_width, PIXEL_SIZE+LINE_WIDTH):
        for pos_y in range(+PIXEL_SIZE//2, c_height, PIXEL_SIZE+LINE_WIDTH):
            x_grid = pos_x // (PIXEL_SIZE + LINE_WIDTH)
            y_grid = pos_y // (PIXEL_SIZE + LINE_WIDTH)
            pixel_value = image.getpixel((x_grid, y_grid))
            colour = "black" if pixel_value > 128 else "white"
            canvas.create_text(pos_x, pos_y, text = f"{hex(pixel_value//16)}", fill=colour, font=(f'Helvetica {PIXEL_SIZE//3}'))    

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
c_width, c_height = calc_canvas_size(X_RES, Y_RES)
canvas = tk.Canvas(root, width=c_width, height=c_height, bg="white", 
                   highlightthickness=0, borderwidth=0) # remove border
for line in range(PIXEL_SIZE, c_width, PIXEL_SIZE+LINE_WIDTH):
    canvas.create_line([(line, 0), (line, c_height)],fill='grey', tags='grid_line_w')
for line in range(PIXEL_SIZE, c_height, PIXEL_SIZE+LINE_WIDTH):
    canvas.create_line([(0, line), (c_width, line)],fill='grey', tags='grid_line_h')
    # draw colour
    for pos_x in range(PIXEL_SIZE//2, c_width, PIXEL_SIZE+LINE_WIDTH):
        for pos_y in range(+PIXEL_SIZE//2, c_height, PIXEL_SIZE+LINE_WIDTH):
            x_grid = pos_x // (PIXEL_SIZE + LINE_WIDTH)
            y_grid = pos_y // (PIXEL_SIZE + LINE_WIDTH)
            pixel_value = image.getpixel((x_grid, y_grid))
            colour = "black" if pixel_value > 128 else "white"
            canvas.create_text(pos_x, pos_y, text = f"{hex(pixel_value//16)}", fill=colour, font=(f'Helvetica {PIXEL_SIZE//3}'))    

canvas.grid(row=4, column=0, columnspan=5)

# Bind mouse events to the canvas
canvas.bind("<B1-Motion>", paint)

# Row5 - log
etr_log = tk.Entry(root)
etr_log.insert("end", "hello log diablo is boring")
etr_log.grid(row=5, column=0, columnspan=5)

# Row6 read pixel value test
pixel_value_label = tk.Label(root, text="pixel value")
pixel_value_label.grid(row=6, column=0, columnspan=5)


# Function to track mouse movement and update pixel value display
def motion(event):
    x_grid = event.x // (PIXEL_SIZE + LINE_WIDTH)
    y_grid = event.y // (PIXEL_SIZE + LINE_WIDTH)
    etr_output.delete("0", "end")
    etr_output.insert("end", f"org:({event.x},{event.y}), grid:({x_grid},{y_grid})")

    # pixel_value_label.config(text=f"org:({event.x},{event.y}), grid:({x_grid},{y_grid})")
    # x, y = event.x, event.y
    # if 0 <= x < 128 and 0 <= y < 128:
        # update_pixel_value(x, y)
    update_pixel_value(x_grid, y_grid)

# Bind the motion event to the canvas
canvas.bind('<Motion>', motion)

# Run the Tkinter event loop
root.mainloop()
