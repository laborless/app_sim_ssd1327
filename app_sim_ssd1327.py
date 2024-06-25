import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageDraw

import MyCanvas

import serial
import serial.tools.list_ports

# Constants
PIXEL_SIZE = 25 # 4
LINE_WIDTH = 1
X_RES = 20 # 128
Y_RES = 20 # 128


# Initialize the main application window
root = tk.Tk()
root.title("Python Paint App")

mycanvas = MyCanvas.MyCanvas(root, X_RES, Y_RES)

def get_pixel_values():
    color_space = colour_var.get()
    pixstr = ""
    is4bit = combo_colour_depth.current() is 0
    if is4bit:
        nNibles = 1
        divRes = 16
    else:
        nNibles = 2
        divRes = 1
    width, height = mycanvas.Resolution
    
    for y in range(height):
        for x in range(width):
            # need to process depends on colour space
            pixstr += "#" # WANT TO start with 0x?
            r,g,b = mycanvas.grid2pixel(x, y)
            r = r // divRes
            g = g // divRes
            b = b // divRes
            if color_space == 0:
                grey = (r+g+b)//3
                pixstr += hex(grey)[2:].zfill(nNibles) # 2 for 8bit
            else :
                if color_space & 1 :
                    pixstr += hex(r)[2:].zfill(nNibles) # 2 for 8bit
                if color_space & 2 :
                    pixstr += hex(g)[2:].zfill(nNibles) # 2 for 8bit
                if color_space & 4 :
                    pixstr += hex(b)[2:].zfill(nNibles) # 2 for 8bit
            
            pixstr += ","

    return pixstr


# Function to update the image when drawing
def paint(event):
    # to do brush color
    mycanvas.paintPoint(event.x, event.y, "black")
    x_grid, y_grid = mycanvas.point2grid(event.x, event.y)

    update_pixel_value(x_grid, y_grid)
    etr_output.delete("0", "end")
    etr_output.insert("end",get_pixel_values())

# Function to update the displayed pixel value
def update_pixel_value(x, y):
    pixel_value = mycanvas.grid2pixel(x, y)
    pixel_value_label.config(text=f"Pixel value: {pixel_value}")

def colour_sel():
#    selection = "You selected the option " + str(var.get())
#    label.config(text = selection)
   pass

def serial_connect():
    ser = serial.Serial('/dev/ttyS1', 19200, timeout=1)
    ser.write(b'Hello World\r\n')
    ser.read_all()
    ser.close()
    print("connect/disconnect")

def onCreate():
    X_RES = int(etr_res_x.get())
    Y_RES = int(etr_res_y.get())
    mycanvas.update(X_RES, Y_RES)

# Row0 - Menu & Buttons
btn_create = tk.Button(root, text="Canvas \u21BB", command=onCreate)
btn_create.grid(row=0, column=0)

btn_import = tk.Button(root, text="Import")
btn_import.grid(row=0, column=1)

btn_export = tk.Button(root, text="Export")
btn_export.grid(row=0, column=2)

comports = list(serial.tools.list_ports.comports(include_links=True))
combo_com = ttk.Combobox(root, values=comports)
combo_com.grid(row=0, column=3)


combo_baud = ttk.Combobox(root, values=["9600","57600"])
combo_baud.grid(row=0, column=4)

btn_connect = tk.Button(root, text="Connect")
btn_connect.grid(row=0, column=5)

# Row1 - Resolution X/Y
lbl_res_x = tk.Label(root, text="res_x",)
lbl_res_x.grid(row=1, column=0)
etr_res_x = tk.Entry(root)
etr_res_x.insert("end", f"{X_RES}")
etr_res_x.grid(row=1, column=1)
lbl_res_y = tk.Label(root, text="res_y")
lbl_res_y.grid(row=1, column=3)
etr_res_y = tk.Entry(root)
etr_res_y.insert("end", f"{Y_RES}")
etr_res_y.grid(row=1, column=4)

# Row2 - CANVAS option
frm_colour = tk.Frame(root)
frm_colour.grid(row=2, column=0, columnspan=4)
colour_var = tk.IntVar()
rad_colour_grey = tk.Radiobutton(frm_colour, text="GREY", variable=colour_var, value=0, command=colour_sel)
rad_colour_grey.grid(row=0, column=0)
rad_colour_rgb = tk.Radiobutton(frm_colour, text="RGB", variable=colour_var, value=7, command=colour_sel)
rad_colour_rgb.grid(row=0, column=1)
rad_colour_red = tk.Radiobutton(frm_colour, text="Red", variable=colour_var, value=1, command=colour_sel)
rad_colour_red.grid(row=0, column=2)
rad_colour_green = tk.Radiobutton(frm_colour, text="Green", variable=colour_var, value=2, command=colour_sel)
rad_colour_green.grid(row=0, column=3)
rad_colour_blue = tk.Radiobutton(frm_colour, text="Blue", variable=colour_var, value=4, command=colour_sel)
rad_colour_blue.grid(row=0, column=4)
rad_colour_grey.select()

combo_colour_depth = ttk.Combobox(frm_colour, values=["4bit","8bit"])
combo_colour_depth.grid(row=0, column=5)
combo_colour_depth.current(0)
   
# Row3 - output
# Create a label to display pixel values
etr_output = tk.Entry(root, width=X_RES*3)
etr_output.insert("end",get_pixel_values())
etr_output.grid(row=3, column=0, columnspan=5)

# Row4 - canvas
# Create a canvas to draw on
# mycanvas = MyCanvas.MyCanvas(root, X_RES, Y_RES)

# Bind mouse events to the canvas
mycanvas.Canvas.bind("<B1-Motion>", paint)
mycanvas.Canvas.bind("<Button-1>", paint)

# Row5 - log
etr_log = tk.Entry(root)
etr_log.insert("end", "org:(0,0), grid:(0,0)")
etr_log.grid(row=5, column=0, columnspan=5)

# Row6 read pixel value test
pixel_value_label = tk.Label(root, text="pixel value")
pixel_value_label.grid(row=6, column=0, columnspan=5)


# Function to track mouse movement and update pixel value display
def motion(event):
    x_grid, y_grid = mycanvas.point2grid(event.x, event.y)
    etr_log.delete("0", "end")
    etr_log.insert("end", f"org:({event.x},{event.y}), grid:({x_grid},{y_grid})")

    # pixel_value_label.config(text=f"org:({event.x},{event.y}), grid:({x_grid},{y_grid})")
    # x, y = event.x, event.y
    # if 0 <= x < 128 and 0 <= y < 128:
        # update_pixel_value(x, y)
    update_pixel_value(x_grid, y_grid)

# Bind the motion event to the canvas
mycanvas.Canvas.bind('<Motion>', motion)


# Run the Tkinter event loop
root.mainloop()
