#Polygon from Hand by Iron Hand
#------------------------------

import pygame, os, subprocess, math
import pygame.locals
import pyfm

pygame.init()
mainClock = pygame.time.Clock()

WINDOWWIDTH = 320
WINDOWHEIGHT = 240
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
pygame.display.set_caption('PyRadio Zero')

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

#Paths
home_path = "/media/home/.pyradio/"
config_name = "pyradio_config"
favorits_name = "pyradio_favorits"
pygame.mouse.set_visible(False)

#Fonts
basic_font_size = 21
basicFont = pygame.font.SysFont(None, basic_font_size)
big_font_size = 35
bigFont = pygame.font.SysFont(None, big_font_size)

#Render Text
render_info_text = basicFont.render('', True, WHITE, BLACK)
info_text_Rect = render_info_text.get_rect()
info_text = [" "," "," "," "," "]

#Globals
menu_index = 0
menu_name = "Main"
menu_list = ["Main","Favorits","Scan"]#,"debug"]

favorits_list = []
favorits_description_list = []
favorit_selector = 0

scan_option = 0
scan_option_index = 0
scan_start = 76
scan_end = 108
scan_steps = 2
scan_quality = 30
bandwide_point_list = []
bandwide_scale = 1

message_box_text = "Welcome!"

master_frequenz = 90.0
master_volume = 10.0
master_brightness = subprocess.check_output(["cat", "/sys/class/backlight/pwm-backlight/brightness"]).replace("\n","")
#info_text.append(str(master_brightness))

user_input = False
user_input_index = 0
user_input_array = []
user_input_string = ""

output_device = "headphone"

def close_fm():
	write_config()
	write_favorits()
	pyfm.fm_off()
	pyfm.set_headphone_source("PCM")
	
def volume_up():
	global master_volume, info_text
	res = pyfm.fm_vol_up()
	info_text.append(res)
	res = res.replace("Setting volume to ","")
	res = res.replace("%","")
	master_volume = float(res)
	
def volume_down():
	global master_volume, info_text
	res = pyfm.fm_vol_down()
	info_text.append(res)
	res = res.replace("Setting volume to ","")
	res = res.replace("%","")
	master_volume = float(res)

def tune_down():
	global info_text, master_volume, master_frequenz, button_y, button_x
	if master_frequenz > 76:
		if button_b == True:
			master_frequenz -= 0.01
		elif button_a == True:
			master_frequenz -= 1.0
		else:
			master_frequenz -= 0.1
		
	info_text.append(pyfm.fm_tune(master_frequenz, master_volume))

def tune_up():
	global info_text, master_volume, master_frequenz, button_y, button_x
	if master_frequenz < 108:
		if button_b == True:
			master_frequenz += 0.01
		elif button_a == True:
			master_frequenz += 1.0
		else:
			master_frequenz += 0.1
		info_text.append(pyfm.fm_tune(master_frequenz, master_volume))

def write_config():
	global master_volume, master_frequenz
	
	file = open(home_path + config_name, 'w+')
	data = "master_frequenz " + str(master_frequenz) + "\n" + "master_volume " + str(master_volume) + "\n"
	file.write(data)
	file.close()
		
def read_config():
	global master_volume, master_frequenz
	try:
		file = open(home_path + config_name, 'r')
	except:
		#File dont exist, so create Folder and File
		try:
			os.mkdir(home_path)
		except:
			pass
		#Init Values
		master_frequenz = 90.0
		master_volume = 10.0
		write_config()
		file = open(home_path + config_name, 'r')
	
	data = file.readlines()
	file.close()
	
	for line in data:
		line = line.replace("\n","")
		if("master_frequenz" in line):
			master_frequenz = float(line.replace("master_frequenz ",""))
		if("master_volume" in line):
			master_volume = float(line.replace("master_volume ",""))

def write_favorits():
	global favorits_list
	
	file = open(home_path + favorits_name, 'w+')
	file.writelines(favorits_list)
	file.close()
	
def read_favorits():
	global favorits_list
	
	try:
		file = open(home_path + favorits_name, 'r')
	except:
		#File dont exist, so create Folder and File
		try:
			os.mkdir(home_path)
		except:
			pass
		write_favorits()
		file = open(home_path + favorits_name, 'r')
	
	favorits_list = file.readlines()
	file.close()

def menu_schedul(index):
	global menu_name, menu_index

	if index >= len(menu_list):
		index = 0
		menu_index = index
	elif index < 0:
		index = len(menu_list) - 1
		menu_index = index
		
	menu_name = menu_list[index]
		
def button_up():
	global user_input
	if user_input == False:
		if(menu_name == "Main" or menu_name == "debug"):
			volume_up()
		elif(menu_name == "Favorits"):
			global favorit_selector
			if favorit_selector > 0:
				favorit_selector -= 1
		
		elif(menu_name == "Scan"):
			global scan_option_index
			
			if scan_option_index > 0:
				scan_option_index -= 1

def button_down():
	global user_input
	if user_input == False:
		if(menu_name == "Main" or menu_name == "debug"):
			volume_down()
		elif(menu_name == "Favorits"):
			global favorit_selector, favorits_list
			if favorit_selector < len(favorits_list)-1:
				favorit_selector += 1
		elif(menu_name == "Scan"):
			global scan_option_index
			
			if scan_option_index < 5:
				scan_option_index += 1
			
def button_left():
	global user_input, user_input_index
	if user_input == False:
		if(menu_name == "Main" or menu_name == "debug"):
			tune_down()
		elif(menu_name == "Scan"):
			global scan_option, message_box_text
			scan_option = 0
			message_box_text = "from current frequenzy"
	else:
		if user_input_index > 0:
			user_input_index -= 1

def button_right():
	global user_input, user_input_index
	if user_input == False:
		if(menu_name == "Main" or menu_name == "debug"):
			tune_up()
		elif(menu_name == "Scan"):
			global scan_option, message_box_text
			scan_option = 1
			message_box_text = "Take a long time!"
	else:
		user_input_index += 1
		
def button_a_fnc():
	global user_input
	if user_input == False:
		if(menu_name == "Favorits"):
			tune_favorit()
		elif(menu_name == "Scan"):
			set_scan_options(1)
	else:
		global favorits_list, user_input_string, favorit_selector
		favorits_list[favorit_selector] = favorits_list[favorit_selector][:6].replace("\n","") + "          " + user_input_string + "\n"
		user_input = False
	
def button_b_fnc():
	global user_input
	if user_input == False:
		if(menu_name == "Scan"):
			set_scan_options(-1)
		elif(menu_name == "Favorits"):
			favorit_down()
	else:
		user_input = False
		
def button_x_fnc():
	if(menu_name == "Main"):
		global bandwide_scale
		if bandwide_scale > 1:
			bandwide_scale -= 1
			fill_bandwide_point_list()
	elif(menu_name == "Scan"):
		set_scan_options(-10)
	elif(menu_name == "Favorits"):
		global user_input, favorits_list, favorit_selector, user_input_string, user_input_array, user_input_index
		if user_input == False:
			user_input_string = ""
			user_input_array = []
			user_input_index = 0
			user_input = True
	
def button_y_fnc():
	if(menu_name == "Main"):
		global bandwide_scale
		bandwide_scale += 1
		fill_bandwide_point_list()
	elif(menu_name == "Scan"):
		set_scan_options(10)
	elif(menu_name == "Favorits"):
		favorit_up()

def button_select_fct():
	if(menu_name == "Main"):
		global master_frequenz
		add_favorit(master_frequenz)
	if(menu_name == "Favorits"):
		global favorit_selector
		del_favorit(favorit_selector)
		if(favorit_selector > 0):
			favorit_selector -= 1
		
def button_start_fct():
	if(menu_name == "Scan"):
		if scan_option == 0:
			global master_frequenz, message_box_text, scan_end, scan_quality
			
			start = master_frequenz + 0.1
			end = scan_end
			
			if start < 76:
				start = 76
			if end > 108:
				end = 108
			
			found_frequenz = 0
			best_qual = 0
			start = int(start*10)
			end = int(end*10)
			break_point = False
			if start < end:
				for i in range(start,end,scan_steps):
					best_qual = pyfm.fm_scan_once_next(i)
					if best_qual >= scan_quality:
						found_frequenz = i/10.0
						break
					
					if i/10.0 > 108 or i/10.0 < 76:
						break
					
					if break_point == True:
						break
					
					for event in pygame.event.get():
						if event.type == pygame.locals.KEYDOWN:
							if event.key == pygame.locals.K_LALT:
								break_point = True
		
			#found_frequenz, quality = pyfm.fm_scan_next(master_frequenz,scan_end,scan_steps,scan_quality)
			
			if found_frequenz >= 76 and break_point == False:
				master_frequenz = found_frequenz
				message_box_text = "Station Found " + str(best_qual) + "%"
			else:
				message_box_text = "No Station Found"
		elif scan_option == 1:
			global master_frequenz, bandwide_point_list, scan_start, scan_end, scan_steps 
			
			bandwide_point_list = []
			
			start = scan_start
			end = scan_end
			
			if start < 76:
				start = 76
			if end > 108:
				end = 108
	
			start = int(start*10)
			end = int(end*10)
			break_point = False
			for i in range(start,end,scan_steps):
				bandwide_point_list.append(pyfm.fm_scan_once_all(i))
				
				if break_point == True:
					break
				
				for event in pygame.event.get():
					if event.type == pygame.locals.KEYDOWN:
						if event.key == pygame.locals.K_LALT:
							break_point = True
				
			#bandwide_point_list = pyfm.fm_scan_all(scan_start, scan_end, scan_steps)
			
			if break_point == False:
				message_box_text = "Scan Complete!"
			else:
				message_box_text = "Scan Canceled!"
			
			#info_text.append(str(len(bandwide_point_list)))
			#info_text.append(str(bandwide_point_list[1]))
			
			for i in range(0,len(bandwide_point_list)):
				bandwide_point_list[i][0] = int(-760+bandwide_point_list[i][0])
				bandwide_point_list[i][1] = int(bandwide_point_list[i][1])
				
			fill_bandwide_point_list()
	elif(menu_name == "Main"):
		global output_device
		if output_device == "headphone":
			output_device = "speaker"
			pyfm.set_headphone_source("PCM")
			pyfm.set_line_out_source("Line In")
			pyfm.set_speaker("on")
		elif output_device == "speaker":
			output_device = "headphone"
			pyfm.set_headphone_source("Line In")
			pyfm.set_line_out_source("PCM")
			pyfm.set_speaker("off")

def set_user_input(direction):
	global user_input_index, user_input_array, user_input_string
	if user_input_index < len(user_input_array):
		char_digit = ord(user_input_array[user_input_index])
		char_digit += direction
		if char_digit < 32:
			char_digit = 126
		if char_digit > 126:
			char_digit = 32
		user_input_array[user_input_index] = chr(char_digit)
	elif user_input_index == len(user_input_array):
		user_input_array.append("`")
		user_input_array[user_input_index] = chr(ord(user_input_array[user_input_index])+direction)
	else:
		for i in range(0,user_input_index - len(user_input_array),1):
			user_input_array.append(" ")
	
	user_input_string = ""
	for char in user_input_array:
		user_input_string += char
		
def set_scan_options(value):
	if scan_option_index == 0:
		global scan_quality
		if( (scan_quality <= 100-value) and (scan_quality > -value) ):
			scan_quality += value
	elif scan_option_index == 1:
		global scan_start
		if( (scan_start <= 108-value) and (scan_start > 75-value) ):
			scan_start += value
	elif scan_option_index == 2:
		global scan_end
		if( (scan_end <= 108-value) and (scan_end > 75-value) ):
			scan_end += value
	elif scan_option_index == 3:
		global scan_steps
		scan_steps += value
		if scan_steps <= 0:
			scan_steps = 1
	elif scan_option_index == 4:
		global point_list_b
		point_list_b = []
		
def tune_favorit():
	global favorits_list, favorit_selector, master_frequenz, master_volume
	
	master_frequenz = float(favorits_list[favorit_selector][:6])
	pyfm.fm_tune(master_frequenz, master_volume)
		
def add_favorit(frequenz):
	global favorits_list, message_box_text
	
	favorits_list.append(str(frequenz) + "\n")
	message_box_text = "Add " + str(frequenz) + " to Favorits"

def del_favorit(index):
	global favorits_list
	
	favorits_list.remove(favorits_list[index])
	
def favorit_up():
	global favorits_list, favorit_selector
	
	if(favorit_selector > 0):
		temp_entry = favorits_list[favorit_selector]
		favorits_list[favorit_selector] = favorits_list[favorit_selector-1]
		favorits_list[favorit_selector-1] = temp_entry
		
		favorit_selector -= 1
		
def favorit_down():
	global favorits_list, favorit_selector
	
	if(favorit_selector < len(favorits_list)-1):
		temp_entry = favorits_list[favorit_selector]
		favorits_list[favorit_selector] = favorits_list[favorit_selector+1]
		favorits_list[favorit_selector+1] = temp_entry
		
		favorit_selector += 1
	
#Render Functions
def render_menu_bar():
	render_menu_bar = basicFont.render(str(menu_index) + "-" + menu_name, True, WHITE, BLACK)
	windowSurface.blit(render_menu_bar, pygame.Rect(2,2,320,basic_font_size))
	pygame.draw.rect(windowSurface, WHITE, pygame.Rect(0,0,320,basic_font_size), 2)
	
	render_frequenz_small(269,1,WHITE,BLACK,WHITE)
	
	for i in range(0,len(menu_list),1):
		pygame.draw.rect(windowSurface, RED, pygame.Rect(menu_index*(320/len(menu_list)),20,320/len(menu_list),1), 2)
	
def render_frequenz(x, y, fcolor, bcolor, rcolor):
	render_master_frequenz = bigFont.render("%0.2f" % master_frequenz, True,fcolor, bcolor)
		
	windowSurface.blit(render_master_frequenz, pygame.Rect(x+5,y+1,100,50))
	pygame.draw.rect(windowSurface, rcolor, pygame.Rect(x,y,85,25), 3)
	
def render_frequenz_button(x,y,r):
	pygame.draw.circle(windowSurface, WHITE, (x, y), r, 2)
	pygame.draw.circle(windowSurface, WHITE, (int(x+(r/1.6 * math.sin(360-master_frequenz))), int(y+(r/1.6 * math.cos(360-master_frequenz)))), r/5, 0)
	
def render_volume_button(x,y,r):
	pygame.draw.circle(windowSurface, WHITE, (x, y), r, 2)
	if(master_volume > 99):
		set_button = 97
	elif(master_volume < 1):
		set_button = 3
	else:
		set_button = master_volume
	pygame.draw.circle(windowSurface, WHITE, (int(x+(r/1.6 * math.sin(-set_button-0.2))), int(y+(r/1.6 * math.cos(-set_button-0.2)))), r/5, 0)
	
def render_frequenz_needle(y):
	pygame.draw.rect(windowSurface, RED, pygame.Rect((-760+master_frequenz*10),y+2,2,240-y), 3)
	#pygame.draw.line(windowSurface, RED, (-760+master_frequenz*10,y), (-760+master_frequenz*10,y+240),3)

def render_frequenz_small(x, y, fcolor, bcolor, rcolor):
	render_master_frequenz = basicFont.render("%0.2f" % master_frequenz, True,fcolor, bcolor)
		
	if master_frequenz >= 100:
		windowSurface.blit(render_master_frequenz, pygame.Rect(x+6,y+3,100,50))
	else:
		windowSurface.blit(render_master_frequenz, pygame.Rect(x+11,y+3,100,50))
	pygame.draw.rect(windowSurface, rcolor, pygame.Rect(x,y,55,19), 2)
	
def render_volume(x, y, fcolor, bcolor, rcolor):
	if master_volume < 100:
		render_master_volume = bigFont.render("%0.2f" % master_volume, True,fcolor, bcolor)
	else:
		render_master_volume = bigFont.render("%0.1f" % master_volume, True,fcolor, bcolor)
		
	windowSurface.blit(render_master_volume, pygame.Rect(x+5,y+1,100,50))
	pygame.draw.rect(windowSurface, rcolor, pygame.Rect(x,y,70,25), 3)
		
def render_favorits_list(select):
	line = basic_font_size
	new_rect = pygame.Rect(5,30,320, 0)
	start_index = 0
	if select > 5:
		start_index = select-5
	
	for fav in favorits_list[start_index:]:
		render_favorits = basicFont.render(str(fav).replace("\n",""), True, WHITE, BLACK)
		windowSurface.blit(render_favorits, new_rect)
		
		new_rect = new_rect.move(0,basic_font_size)
		line += basic_font_size	
	
	if select < 5:
		pygame.draw.rect(windowSurface, RED, pygame.Rect(2,25 + (select*basic_font_size),315,basic_font_size), 2)
	else:
		pygame.draw.rect(windowSurface, RED, pygame.Rect(2,25 + (5*basic_font_size),315,basic_font_size), 2)
	
def render_message_box(text):
	render_text_box = basicFont.render(str(text), True, WHITE, BLACK)
		
	windowSurface.blit(render_text_box, pygame.Rect(80,4,100,basic_font_size))
	#pygame.draw.rect(windowSurface, rcolor, pygame.Rect(x,y,70,25), 3)
	
def render_frequenz_scala(y):
	
	point_list = []
	for i in range(760,1080,10):
		#point_list.append( ((-760+i,y), (-760+i,y+240)) )
		
		point_list.append( (-760+i,y) )
		point_list.append( (-760+i,y+240) )
		point_list.append( (-760+i,y) )
	
	#pygame.draw.line(windowSurface, GRAY, (-760+i,y), (-760+i,y+240),1)
	pygame.draw.lines(windowSurface, GRAY, False, point_list, 1)
	
	pygame.draw.rect(windowSurface, WHITE, pygame.Rect(0,y,320,240-y), 2)

point_list_b = []	
def render_bandwide_analysis(fcolor):
	if len(point_list_b) > 0:		
		#pygame.draw.rect(windowSurface, fcolor, pygame.Rect(i[0],235,1,-i[1]), 1)
		#pygame.draw.line(windowSurface, fcolor, (i[0],238), (i[0],238-(i[1]*bandwide_scale)), 1)
		pygame.draw.lines(windowSurface, fcolor, False, point_list_b, 1)

def fill_bandwide_point_list():
	global point_list_b
	point_list_b = []
	for i in bandwide_point_list:
		point_list_b.append( (i[0],238) )
		point_list_b.append( (i[0],238-(i[1]*bandwide_scale)) )
		point_list_b.append( (i[0],238) )
		
def render_input_box():
	global user_input_string, user_input_index
	
	pygame.draw.rect(windowSurface, BLACK, pygame.Rect(20,100,280,basic_font_size), 0)
	pygame.draw.rect(windowSurface, WHITE, pygame.Rect(20,100,280,basic_font_size), 3)
	
	render_text_box = basicFont.render(user_input_string, True, WHITE, BLACK)
	#text_Rect = render_text_box.get_rect()
	windowSurface.blit(render_text_box, pygame.Rect(25,102,280,basic_font_size))
	
	pygame.draw.rect(windowSurface, RED, pygame.Rect(25+8*user_input_index,117,8,2), 0)
		
#Read In Config File
read_config()
read_favorits()
#favorits_list = ["90.0\n","91.5\n"]

#Alsa Mixer Headphone Source to Line In
pyfm.set_headphone_source("Line In")

#Put Device ON
res = pyfm.fm_on()
if("Radio on" in res):
	info_text.append(res)
else:
	close_fm()
	pygame.quit()
	
#Tune to last Settings
pyfm.fm_tune(master_frequenz, master_volume)	

button_up_state = False
button_down_state = False
button_left_state = False
button_right_state = False
button_a = False
button_b = False
button_x = False
button_y = False
button_pause = False
button_select = False
button_left_shoulder = False
	
#Game Loop
while True:

	for event in pygame.event.get():
		#Quit Event
		if event.type == pygame.locals.QUIT:
			close_fm()
			pygame.quit()
		if event.type == pygame.locals.KEYDOWN and button_pause == False:
			#info_text.append(str(event.key))
			if event.key == pygame.locals.K_UP:
				button_up_state = True
				button_up()
			if event.key == pygame.locals.K_DOWN:
				button_down_state = True
				button_down()
			if event.key == pygame.locals.K_LEFT:
				button_left_state = True
			if event.key == pygame.locals.K_RIGHT:
				button_right_state = True
				
			#Left Shoulder
			if event.key == pygame.locals.K_TAB:
				button_left_shoulder = True
				menu_index -= 1
				info_text.append("Menu_index:" + str(menu_index))
				menu_schedul(menu_index)
				message_box_text = ""
			#Right Shoulder
			if event.key == pygame.locals.K_BACKSPACE:
				menu_index += 1
				info_text.append("Menu_index:" + str(menu_index))
				menu_schedul(menu_index)
				message_box_text = ""
				
			#a,b,x,y Buttons Press
			if event.key == pygame.locals.K_LCTRL:
				button_a = True
			if event.key == pygame.locals.K_LALT:
				button_b = True
			if event.key == pygame.locals.K_SPACE:
				button_y = True
			if event.key == pygame.locals.K_LSHIFT:
				button_x = True
				
			#Select Button
			if event.key == pygame.locals.K_ESCAPE:
				button_select = True
				button_select_fct()
			#Start Button
			if event.key == pygame.locals.K_RETURN:
				if(menu_name == "Scan"):
					if scan_option == 0:
						message_box_text = "Scanning Next Station!"
					else:
						message_box_text = "Scanning All Stations!"
			#Pause Button
			if event.key == pygame.locals.K_PAUSE:
				button_pause = True
				subprocess.Popen("echo -n 0 > /sys/class/backlight/pwm-backlight/brightness", shell=True)
					
		if event.type == pygame.locals.KEYUP:
			if button_pause == False:
				#Exit
				if event.key == pygame.locals.K_HOME:
					if button_left_shoulder == False:
						close_fm()
					else:
						write_config()
					pygame.quit()
				if event.key == pygame.locals.K_UP:
					button_up_state = False
				if event.key == pygame.locals.K_DOWN:
					button_down_state = False
				if event.key == pygame.locals.K_LEFT:
					button_left_state = False
				if event.key == pygame.locals.K_RIGHT:
					button_right_state = False
				#a,b,x,y Buttons Release
				if event.key == pygame.locals.K_LCTRL:
					button_a = False
					button_a_fnc()
				if event.key == pygame.locals.K_LALT:
					button_b = False
					button_b_fnc()
				if event.key == pygame.locals.K_SPACE:
					button_y = False
					button_y_fnc()
				if event.key == pygame.locals.K_LSHIFT:
					button_x = False
					button_x_fnc()
				
				if event.key == pygame.locals.K_RETURN:
					button_start_fct()
				if event.key == pygame.locals.K_ESCAPE:
					button_select = False	
				if event.key == pygame.locals.K_TAB:
					button_left_shoulder = False
			#Pause OFF
			if event.key == pygame.locals.K_PAUSE:
				button_pause = False
				subprocess.Popen("echo -n " + str(master_brightness) + " > /sys/class/backlight/pwm-backlight/brightness", shell=True)
			
	#Buttons Hold DOWN
	if button_left_state == True:
		button_left()
	if button_right_state == True:
		button_right()
		
	if button_up_state == True:
		if user_input == True:
			set_user_input(1)
	if button_down_state == True:
		if user_input == True:
			set_user_input(-1)
				
				
	#Clear Screen
	windowSurface.fill(BLACK)
	
	if button_pause == False:
		#All Renerers-------------------------------------------------------
		render_menu_bar()
		#fmtools debug Render
		if(menu_name == "debug"):
			line = basic_font_size
			for mes in info_text[len(info_text)-3:]:
				new_rect = info_text_Rect.move(0,basic_font_size*3 - line + 174)
				if line == basic_font_size*3:
					render_info_text = basicFont.render(mes, True, RED, BLACK)
				else:
					render_info_text = basicFont.render(mes, True, WHITE, BLACK)
					
				windowSurface.blit(render_info_text, new_rect)
				line += basic_font_size
			
			if len(info_text) > 5:
				del info_text[0]
		
			pygame.draw.rect(windowSurface, WHITE, pygame.Rect(0,174,320,basic_font_size*3), 1)
		#--------------------------------------------------------------------
		#Main Radio Menu
		if(menu_name == "Main"):
			render_frequenz(60,50,WHITE,BLACK,WHITE)
			render_frequenz_button(95,110,25)
			render_frequenz_needle(150)
			render_frequenz_scala(150)
			render_bandwide_analysis(GREEN)
			render_volume(180,50,WHITE,BLACK,WHITE)
			render_volume_button(215,110,25)
			
			for ent in favorits_list:
				if str(master_frequenz) in ent:
					ent = ent[14:].replace("\n","")
					#ent = ent.replace(" ","")
					render_station_name = basicFont.render(ent, True, WHITE, BLACK)
					text_Rect = render_station_name.get_rect()
					windowSurface.blit(render_station_name, pygame.Rect(160-text_Rect.width/2,30,310,basic_font_size))
		
		#Favorits List Menu
		if(menu_name == "Favorits"):
			#render_frequenz_small(120,25,WHITE,BLACK,WHITE)
			render_favorits_list(favorit_selector)
			
		#Scaning Menu
		if(menu_name == "Scan"):
			render_scan_options = basicFont.render("Scan Next Station    Scan All Stations", True, WHITE, BLACK)
			windowSurface.blit(render_scan_options, pygame.Rect(25,30,310,basic_font_size))
			
			pygame.draw.rect(windowSurface, RED, pygame.Rect(15+(140*scan_option),26,140,basic_font_size), 2)
			
			#Options
			render_scan_suboptions = basicFont.render("Quality:                                 " + str(scan_quality) + " %", True, WHITE, BLACK)
			windowSurface.blit(render_scan_suboptions, pygame.Rect(25,60,310,basic_font_size))
			
			render_scan_suboptions = basicFont.render("Start  :                                 " + str(scan_start) + " Mhz", True, WHITE, BLACK)
			windowSurface.blit(render_scan_suboptions, pygame.Rect(25,60+basic_font_size,310,basic_font_size))
			
			render_scan_suboptions = basicFont.render("End    :                                 " + str(scan_end) + " Mhz", True, WHITE, BLACK)
			windowSurface.blit(render_scan_suboptions, pygame.Rect(25,60+basic_font_size*2,310,basic_font_size))
			
			render_scan_suboptions = basicFont.render("Steps  :                                 " + str(scan_steps/10.0) + " Mhz", True, WHITE, BLACK)
			windowSurface.blit(render_scan_suboptions, pygame.Rect(25,60+basic_font_size*3,310,basic_font_size))
			
			render_scan_suboptions = basicFont.render("Delete Scan                              ", True, WHITE, BLACK)
			windowSurface.blit(render_scan_suboptions, pygame.Rect(25,60+basic_font_size*4,310,basic_font_size))
			
			pygame.draw.rect(windowSurface, RED, pygame.Rect(15,56+basic_font_size*scan_option_index,275,basic_font_size), 2)
			
			render_bandwide_analysis(RED)
				
		#Message Box
		if(len(message_box_text) > 0):
			render_message_box(message_box_text)
			
		if user_input == True:
			render_input_box()
		
	#Zeiche alles auf den Schirm
	pygame.display.update()
	mainClock.tick(10)