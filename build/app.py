import AppUI

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
		appUi.entry_color.delete("0", "end")
		appUi.entry_color.insert("0", pixstr)
		appUi.entry_coor.delete("0", "end")
		appUi.entry_coor.insert("0", f"({grid_x},{grid_y})")

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
		


if __name__ == "__main__":
	# load ui
	appUi = AppUI.AppUI()

	# implementation Fcn
	appUi.canvas.bind("<B1-Motion>", paint_display)
	appUi.canvas.bind('<Motion>', hover_display)

	appUi.run()
