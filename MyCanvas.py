import tkinter as tkint
import tkinter.messagebox as messagebox
from tkinter import ttk
from PIL import Image, ImageTk, ImageDraw

class MyCanvas:
    __COLOR_DEPTH_4_ = 0
    __COLOR_DEPTH_8_ = 1

    pixel_size = 25
    line_width = 1

    _x_res = 20
    _y_res = 20

    __color_depth__ = __COLOR_DEPTH_4_    #0: 4bit, else:

    @property
    def Resolution(self):
        return (self._x_res, self._y_res)

    @property
    def Canvas(self):
        return self.canvas
    
    @property
    def color_depth(self):
        return self.__color_depth__

    @color_depth.setter
    def color_depth(self, val):
        if val > 0:
            self.__color_depth__ = MyCanvas.__COLOR_DEPTH_8_
        else:
            self.__color_depth__ = MyCanvas.__COLOR_DEPTH_4_

    # image = Image.new("RGB", (_x_res, _y_res), "white")
    # image_draw = ImageDraw.Draw(image)
    def __init__(self, root: tkint, xres, yres):
        self.image = Image.new("RGB", (xres, yres), "white")
        self.image_draw = ImageDraw.Draw(self.image)

        w, h = self.__calc_size__() 
        self.canvas = tkint.Canvas(root, width=w, height=h, bg="white", highlightthickness=0, borderwidth=0)
        self.update(xres, yres)

    def __bind__(self):
        pass

    def __refresh_image__(self):
        self.image = Image.new("RGB", (self._x_res, self._y_res), "white")
        self.image_draw = ImageDraw.Draw(self.image)

    def __refresh_grid__(self):
        c_width, c_height = self.__calc_size__()
        self.canvas.config(width=c_width, height=c_height)
        # draw_grid
        for line in range(self.pixel_size, c_width, self.pixel_size + self.line_width):
            self.canvas.create_line([(line, 0), (line, c_height)],fill='grey', tags='grid_line_w')
        for line in range(self.pixel_size, c_height, self.pixel_size + self.line_width):
            self.canvas.create_line([(0, line), (c_width, line)],fill='grey', tags='grid_line_h')

        self.canvas.grid(row=4, column=0, columnspan=5)

    def __calc_size__(self):
        width = self._x_res * self.pixel_size + (self._x_res - 1) * self.line_width
        height = self._y_res * self.pixel_size + (self._y_res - 1) * self.line_width
        
        return (width, height)

    def update(self, xres, yres):
        self._x_res = xres
        self._y_res = yres

        self.__refresh_grid__()
        self.__refresh_image__()
    
    # @param x mouse x position
    # @param y mouse y position
    def point2pixel(self, px, py):
        x, y = self.point2grid(px, py)

        return self.grid2pixel(x, y)

    def point2grid(self, px, py):
        x_grid = px // (self.pixel_size + self.line_width)
        y_grid = py // (self.pixel_size + self.line_width)

        return (x_grid, y_grid)

    def grid2pixel(self, grid_x, grid_y):
        return self.image.getpixel((grid_x, grid_y))
    
    def paintPoint(self, px, py, color: str):
        x_grid, y_grid = self.point2grid(px, py)
        self.image_draw.point([(x_grid, y_grid)], fill=color)

        x_st = x_grid * (self.pixel_size + self.line_width)
        y_st = y_grid * (self.pixel_size + self.line_width)
        self.canvas.create_rectangle(
            x_st,
            y_st,
            x_st + self.pixel_size,
            y_st + self.pixel_size,
            fill=color,
            width=0
        )
    
    def getPixelValues(self):
        colour_var = tkint.IntVar()
        color_space = colour_var.get()
        pixstr = ""
        is4bit = self.__color_depth__ is MyCanvas.__COLOR_DEPTH_4_
        if is4bit:
            nNibles = 1
            divRes = 16
        else:
            nNibles = 2
            divRes = 1
        width, height = self.Resolution
        
        for y in range(height):
            for x in range(width):
                # need to process depends on colour space
                pixstr += "#" # WANT TO start with 0x?
                r,g,b = self.grid2pixel(x, y)
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

  