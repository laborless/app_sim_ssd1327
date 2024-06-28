import AppUI
from tkinter import messagebox,colorchooser,filedialog
from PIL import ImageColor, Image
import serial.tools.list_ports
import json


def get_pixel_value_string():
	# color_space = colour_var.get()
	pixstr = ""
	# is4bit = combo_colour_depth.current() is 0
	# if is4bit:
	# 		nNibles = 1
	# 		divRes = 16
	# else:
	# 		nNibles = 2
	# 		divRes = 1
	nNibles = 2
	divRes = 1
	width, height = appUi.image.size

	for y in range(height):
			for x in range(width):
					# need to process depends on colour space
					pixstr += "#" # WANT TO start with 0x?
					r,g,b = appUi.image.getpixel((x, y))
					r = r // divRes
					g = g // divRes
					b = b // divRes
					# if color_space == 0:
					# 		grey = (r+g+b)//3
					# 		pixstr += hex(grey)[2:].zfill(nNibles) # 2 for 8bit
					# else :
					# 		if color_space & 1 :
					# 				pixstr += hex(r)[2:].zfill(nNibles) # 2 for 8bit
					# 		if color_space & 2 :
					# 				pixstr += hex(g)[2:].zfill(nNibles) # 2 for 8bit
					# 		if color_space & 4 :
					# 				pixstr += hex(b)[2:].zfill(nNibles) # 2 for 8bit
					pixstr += hex(r)[2:].zfill(nNibles) # 2 for 8bit
					pixstr += hex(g)[2:].zfill(nNibles) # 2 for 8bit
					pixstr += hex(b)[2:].zfill(nNibles) # 2 for 8bit
					
					pixstr += ","

	return pixstr

def output_color_string():
	out_str = get_pixel_value_string()
	appUi.entry_output.delete("1.0", "end")
	appUi.entry_output.insert('end', out_str)


def hover_display(event):
	color = appUi.get_brush_color()
	line_width = appUi.get_display_line_width()
	disp_pos_x, disp_pos_y = appUi.get_display_offset()
	
	disp_pos_x += appUi.disp_offset[0]
	disp_pos_y += appUi.disp_offset[1]

	if event.x > disp_pos_x \
		  and event.x < disp_pos_x + appUi.disp_width \
			and event.y > disp_pos_y \
			and event.y < disp_pos_y + appUi.disp_height :
		grid_x = (event.x - disp_pos_x - line_width) // (appUi.disp_pixel[0] + line_width)
		grid_y = (event.y - disp_pos_y - line_width) // (appUi.disp_pixel[1] + line_width)

		pixstr = ""
		# is4bit = combo_colour_depth.current() is 0
		# if is4bit:
		# 		nNibles = 1
		# 		divRes = 16
		# else:
		# 		nNibles = 2
		# 		divRes = 1
		nNibles = 2
		divRes = 1
		pixstr += "#"
		r,g,b = appUi.image.getpixel((grid_x, grid_y))
		r = r // divRes
		g = g // divRes
		b = b // divRes
		# if color_space == 0:
		# 		grey = (r+g+b)//3
		# 		pixstr += hex(grey)[2:].zfill(nNibles) # 2 for 8bit
		# else :
		# 		if color_space & 1 :
		# 				pixstr += hex(r)[2:].zfill(nNibles) # 2 for 8bit
		# 		if color_space & 2 :
		# 				pixstr += hex(g)[2:].zfill(nNibles) # 2 for 8bit
		# 		if color_space & 4 :
		# 				pixstr += hex(b)[2:].zfill(nNibles) # 2 for 8bit
		pixstr += hex(r)[2:].zfill(nNibles) # 2 for 8bit
		pixstr += hex(g)[2:].zfill(nNibles) # 2 for 8bit
		pixstr += hex(b)[2:].zfill(nNibles) # 2 for 8bit
		# update position info.
		appUi.entry_color_var.set(pixstr)
		appUi.entry_coor_var.set(f"({grid_x},{grid_y})")

def paint_display(event):
	color = appUi.get_brush_color()
	line_width = appUi.get_display_line_width()
	disp_pos_x, disp_pos_y = appUi.get_display_offset()
	
	disp_pos_x += appUi.disp_offset[0]
	disp_pos_y += appUi.disp_offset[1]

	if event.x > disp_pos_x \
		  and event.x < disp_pos_x + appUi.disp_width \
			and event.y > disp_pos_y \
			and event.y < disp_pos_y + appUi.disp_height :
		grid_x = (event.x - disp_pos_x - line_width) // (appUi.disp_pixel[0] + line_width)
		grid_y = (event.y - disp_pos_y - line_width) // (appUi.disp_pixel[1] + line_width)
		
		# drawing
		x_st = disp_pos_x + line_width + ( grid_x * (appUi.disp_pixel[0] + line_width) )
		y_st = disp_pos_y + line_width + ( grid_y * (appUi.disp_pixel[1] + line_width) )
		appUi.canvas.create_rectangle(x_st, y_st, x_st + appUi.disp_pixel[0],
								y_st + appUi.disp_pixel[1], fill=color, width=0)
		
		# paint in image object
		appUi.image_draw.point([(grid_x, grid_y)], fill=color)

		# update output
		output_color_string()
		
def test(event):
	# TODO:
	# 1. ask to export?
	try:
		res = (appUi.entry_res_x_var.get(), appUi.entry_res_y_var.get())
		if res[0] > 0 and res[0] <= appUi.disp_limit[0] and res[1] > 0 and res[1] <= appUi.disp_limit[1]:
			appUi.disp_resolution = res
			appUi.new_image()
			appUi.render_display()
			output_color_string()
		else:
			messagebox.showerror(title="Error", message=f"resolution! out of range({appUi.disp_limit[0]},{appUi.disp_limit[1]})")
	except Exception as e:
		messagebox.showerror(title="Error", message="Please verify resolution!")

def re_render_display_test():
	# Empty grid display
	appUi.render_display()

	# Draw All Image --> we need this function
	line_width = appUi.get_display_line_width()

	color = appUi.get_brush_color()
	
	disp_pos_x, disp_pos_y = appUi.get_display_offset()
	
	disp_pos_x += appUi.disp_offset[0]
	disp_pos_y += appUi.disp_offset[1]

	for x in range(appUi.disp_resolution[0]):
		for y in range(appUi.disp_resolution[1]):
			
			color = '#%02x%02x%02x' % appUi.image.getpixel((x, y))
			# drawing
			x_st = disp_pos_x + line_width + ( x * (appUi.disp_pixel[0] + line_width) )
			y_st = disp_pos_y + line_width + ( y * (appUi.disp_pixel[1] + line_width) )
			appUi.canvas.create_rectangle(x_st, y_st, x_st + appUi.disp_pixel[0],
									y_st + appUi.disp_pixel[1], fill=color, width=0)

	# update output
	output_color_string()

def apply_brush_color(strColor):
	l = ImageColor.getcolor(strColor, "L")
	fg_color = "black" if l > 128 else "white"
	appUi.entry_brush_var.set(strColor)
	appUi.entry_brush.configure(state="readonly", fg=fg_color, readonlybackground=strColor)
	appUi.set_brush_color(strColor)

def choose_brush_color(event):
	color = colorchooser.askcolor(title="Choose the brush color",initialcolor=appUi.get_brush_color())
	if color[1] is not None:
		apply_brush_color(color[1])


def import_file(event):
	path = filedialog.askopenfilename(title='Import')
	if path:
		isImage = True
		try:
			with Image.open(path) as im:
				print("format", im.format)
				im = im.convert('RGB')
				appUi.image.close()
				appUi.image = im.resize((appUi.disp_resolution[0], appUi.disp_resolution[1]))
				re_render_display_test() # to be replaced to good one
		except:
			isImage = False
		
		if not isImage:
			try:
				with open(path, 'r') as f:
					img = json.load(f)
					print(img)
					# TODO: Need to draw image from test color map
					# re_render_display_test() # to be replaced to good one
			except:
				print("bad input")
				pass

def export_file(event):
	path = filedialog.asksaveasfilename(title='Export')
	if path:
		with open(path, 'w+') as f:
			img = {}
			img["width"] = appUi.image.width
			img["height"] = appUi.image.height
			img["space"] = appUi.combo_colorspace.get()
			img["depth"] = appUi.combo_colordepth.get()
			img["NbRemap"] = appUi.check_nb_remap_var.get()
			img["image"] = [] # to be implemented
			json.dump(img, f)


def connect_driver(event):
	port = appUi.combo_ser_port.get()
	baud = appUi.combo_ser_baudrate.get()
	if baud.isnumeric():
		print(f"connect to {port} in {baud}bps")
		print(f"connecting...")

if __name__ == "__main__":
	# load ui
	appUi = AppUI.AppUI()

	# implementation Fcn
	appUi.canvas.bind("<B1-Motion>", paint_display)
	appUi.canvas.bind('<Motion>', hover_display)
	appUi.button_new.bind("<ButtonRelease-1>", test)

	appUi.entry_coor.configure(state="readonly", readonlybackground="white")
	appUi.entry_color.configure(state="readonly", readonlybackground="white")

	# button import
	appUi.button_import.bind("<ButtonRelease-1>", import_file)
	# button export
	appUi.button_export.bind("<ButtonRelease-1>", export_file)
	# button connect
	appUi.button_connect.bind("<ButtonRelease-1>", connect_driver)

	# Brush color
	appUi.entry_brush.bind("<Button>", choose_brush_color)
	apply_brush_color(appUi.get_brush_color())

	# Color Space
	appUi.combo_colorspace.configure(
			values=["RGB","Red","Green","Blue","Grey"], state="readonly") # background color?
	appUi.combo_colorspace.current(0)

	# Color Depth"
	appUi.combo_colordepth.configure(values=["8bits","4bits"], state="readonly") # background color?
	appUi.combo_colordepth.current(0)

	# Com Port
	comports = list(serial.tools.list_ports.comports(include_links=True))
	appUi.combo_ser_port.configure(values=comports)
	appUi.combo_ser_port.current(0)

	# BaudRate
	baud = ['4800','9600','19200','38400','57600','115200','230400','460800','921600']
	appUi.combo_ser_baudrate.configure(values=baud)
	appUi.combo_ser_baudrate.current(0)

	appUi.run()
