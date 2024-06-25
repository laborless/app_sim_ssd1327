import tkinter as tkint
import tkinter.messagebox as messagebox
from tkinter import ttk
from PIL import Image, ImageTk, ImageDraw

class MyCanvas:
    pixel_size = 25
    line_width = 1

    _x_res = 20
    _y_res = 20

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

    # temporary use only
    # todo:
    # create paint private method to update automatically on mouse events
    def getCanvas(self):
        return self.canvas

    # temporary use only
    # todo:
    # create paint private method to update automatically on mouse events
    def getImage(self):
        return self.image

    # temporary use only
    # todo:
    # create paint private method to update automatically on mouse events
    def getImageDraw(self):
        return self.image_draw