import AppUI
from tkinter import messagebox,colorchooser,filedialog
from PIL import ImageColor, Image
import serial.tools.list_ports
import json
import math

FILL_COLOR = "white"
LIMIT_PHYS_X = 32
LIMIT_PHYS_Y = 32

pixel_string = " "
pixel_string_seperator = ","

# returns -1 if overflow or outof indxex
def find_nth(haystack: str, needle: str, n: int) -> int:
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start+len(needle))
        n -= 1
    return start 

def regen_pixel_value_string():
	global pixel_string
	pixel_string = get_pixel_value_string()

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
					# pixstr += "#" # WANT TO start with 0x?
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
					
					pixstr += pixel_string_seperator

	return pixstr

def get_pixel_value_string_at(x, y):
	pixstr = ""
	nNibles = 2
	divRes = 1
	# need to process depends on colour space
	# pixstr += "#" # WANT TO start with 0x?
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
	
	# pixstr += ","

	return pixstr
# @param x grid x
# @paramy grid y
def output_color_string_at(x, y):
	
	width, height = appUi.image.size

	nth = y * width + x
	
	replace_start_idx = find_nth(pixel_string, pixel_string_seperator, nth) + 1
	# if find_nth returns -1, possible solution is that it was end of idx
	if replace_start_idx == 0:
		messagebox.showerror("output_color_string_at error", "find_nth returned -1. handle this please")	
		return

	size = find_nth(pixel_string, pixel_string_seperator, 1)
	value = get_pixel_value_string_at(x, y)
	appUi.entry_output.delete("1." + str(replace_start_idx), "1." + str(replace_start_idx + size))
	appUi.entry_output.insert("1." + str(replace_start_idx), value)

def output_color_string():
	out_str = get_pixel_value_string()
	appUi.entry_output.delete("1.0", "end")
	appUi.entry_output.insert('end', out_str)
	global pixel_string
	pixel_string = out_str


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
		output_color_string_at(grid_x, grid_y)
		
def test(event):
	# TODO:
	# 1. ask to export?
	try:
		res = (appUi.entry_res_x_var.get(), appUi.entry_res_y_var.get())
		if res[0] > LIMIT_PHYS_X or res[1] > LIMIT_PHYS_Y:
			messagebox.showerror(title="Error", message=f"resolution! out of range({LIMIT_PHYS_X},{LIMIT_PHYS_Y})")
			return	
			
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
def test2(event):
	val = 1
	strr = "1." + str(val)
	messagebox.showinfo(val, strr)
	# tmp = "1,2,3,4,5,6,7,8,9,0,"
	
	# appUi.entry_output.insert("1.0", tmp)
	# idx = find_nth(tmp, ",", 1)
	# messagebox.showinfo("test2", tmp)
	# # appUi.entry_output.delete("1.0", "2.0")
	# appUi.entry_output.replace("1.1", "1.3", "added")
	# # appUi.entry_output.insert("1.0", "added")
	# messagebox.showinfo("test2", appUi.entry_output.get("1.0", "end"))


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
					jsn = json.load(f)
					# TODO: Need to draw image from test color map
					# re_render_display_test() # to be replaced to good one
					w = jsn.pop('width')
					h = jsn.pop('height')
					img = jsn.pop('image')
					appUi.entry_res_x_var.set(w)
					appUi.entry_res_y_var.set(h)
					
					test(event=None)
					cnt = 0
					for pixstr in img.split(','):
						val = int(pixstr, 16)
						pixval = (val & 255, val >> 8 & 255, val >> 16 & 255)
						appUi.set_image(cnt % w, cnt / w, pixval)
						cnt += 1
						if cnt >= w * h:
							break
						
					# update display
					re_render_display_test()

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
			img["image"] = pixel_string
			json.dump(img, f)


def move_image(st, end):
	line_width = appUi.get_display_line_width()
	dist = ((st[0]-end[0])/(appUi.disp_pixel[0]+line_width), (st[1]-end[1])/(appUi.disp_pixel[1]+line_width))
	appUi.image = appUi.image.transform((appUi.image.width, appUi.image.height),
									  Image.AFFINE, (1, 0, dist[0], 0, 1, dist[1]),
										fill=1 ,fillcolor = FILL_COLOR)

def rotate_image(st, end):
	line_width = appUi.get_display_line_width()
	grid_offset = appUi.get_display_offset() # need to change name ..it's confusing
	center = ((appUi.disp_offset[0]+grid_offset[0]+appUi.disp_width//2), (appUi.disp_offset[1]+grid_offset[1]+appUi.disp_height//2))
	
	vect1 = ((st[0]-center[0])/(appUi.disp_pixel[0]+line_width), (st[1]-center[1])/(appUi.disp_pixel[1]+line_width))
	vect2 = ((end[0]-center[0])/(appUi.disp_pixel[0]+line_width), (end[1]-center[1])/(appUi.disp_pixel[1]+line_width))

	angle = math.degrees(math.atan2(vect1[1],vect1[0]) - math.atan2(vect2[1],vect2[0]) )

	appUi.image = appUi.image.rotate(angle, fillcolor = FILL_COLOR)


# Is ther better way instead of using global variable?
pos_start = None

def canvas_enter(event):
	print("canvas enter")
def canvas_leave(event):
	global pos_start
	pos_start= None
	# print("canvas leave")

def canvas_LeftButtonDown(event):
	global pos_start
	pos_start = (event.x, event.y)


def canvas_LeftButtonUp(event):
	global pos_start
	if pos_start:
		mode = appUi.combo_control_mode.current()
		if mode == 2 :
			move_image(pos_start, (event.x, event.y))
		elif mode == 3 :
			rotate_image(pos_start, (event.x, event.y))

		re_render_display_test() # to be replaced to good one

	pos_start = None

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
	# appUi.canvas.bind('<Button-1>', paint_display)

	# appUi.canvas.bind("<Enter>", canvas_enter)
	appUi.canvas.bind("<Leave>", canvas_leave)
	appUi.canvas.bind("<Button-1>", canvas_LeftButtonDown)
	appUi.canvas.bind("<ButtonRelease-1>", canvas_LeftButtonUp)


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

	# Control mode
	control_modes = ['Inspect','Paint','Move','Rotate']
	appUi.combo_control_mode.configure(values=control_modes, state="readonly") # background color?
	appUi.combo_control_mode.current(0)

	# Com Port
	comports = list(serial.tools.list_ports.comports(include_links=True))
	appUi.combo_ser_port.configure(values=comports)
	appUi.combo_ser_port.current(0)

	# BaudRate
	baud = ['4800','9600','19200','38400','57600','115200','230400','460800','921600']
	appUi.combo_ser_baudrate.configure(values=baud)
	appUi.combo_ser_baudrate.current(0)

	output_color_string()
	appUi.run()
