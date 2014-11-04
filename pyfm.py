#PyFM - Python Funktions to control fmtools by Kay Wenzel 2014
#-------------------------------------------------------------

#This is made for the GCW Zero where the device is /dev/radio0
#It use the default device values of fm and fmscan device_index = 0, device_typ = 1
#You can use the return values to parse information in your GUI or somwhere else

import subprocess

def fm_on():
	return subprocess.check_output(["fm", "on"]).replace("\n","")
	
def fm_off():
	return subprocess.check_output(["fm", "off"]).replace("\n","")
	
def fm_tune(frequenz, volume):
	try:
		output = subprocess.check_output(["fm", str(frequenz), str(volume)]).replace("\n","")
	except:
		output = "Frequenz out of range."

	return output

def fm_vol_up():
	return subprocess.check_output(["fm", "+"]).replace("\n","")
	
def fm_vol_down():
	return subprocess.check_output(["fm", "-"]).replace("\n","")
	
def fm_scan_all_stations():
	res = subprocess.check_output(["fmscan"]).replace("\n","")
	
def set_headphone_source(source):
	#source = "Line In", "PCM"
	subprocess.Popen("amixer sset 'Headphone Source',0 '" + source + "'", shell=True)

def set_line_out_source(source):
	#source = "Line In", "PCM"
	subprocess.Popen("amixer sset 'Line Out Source',0 '" + source + "'", shell=True)
	
def set_speaker(state):
	if state == "on":
		subprocess.Popen("amixer sset 'Speakers',0 'on'", shell=True)
	elif state == "off":
		subprocess.Popen("amixer sset 'Speakers',0 'off'", shell=True)
	
def fm_scan_next(start, end, steps, min_quality):
	
	if start < 76:
		start = 76
	if end > 108:
		end = 108
	
	frequenz = 0
	start = int(start*10)
	end = int(end*10)
	if start > end:
		return 0, 0
	for i in range(start,end,steps):
		res = subprocess.check_output(["fmscan", "-s " + str(i/10.0), "-e " + str(i/10.0)]).replace("\n","")
		res_sp = res.split("\r")
		
		best_qual = 0
		for j in res_sp:
			if "checking" in j:
				qual = j[j.index("g:")+3:j.index("%")]
				best_qual = max(float(qual), best_qual)
		
		if best_qual >= min_quality:
			frequenz = i/10.0
			break
		
		if i/10.0 > 108 or i/10.0 < 76:
			break
	
	return frequenz, best_qual
	
def fm_scan_all(start, end, steps):

	if start < 76:
		start = 76
	if end > 108:
		end = 108
	
	quality_list = []
	
	start = int(start*10)
	end = int(end*10)
	for i in range(start,end,steps):
		res = subprocess.check_output(["fmscan", "-s " + str(i/10.0), "-e " + str(i/10.0)]).replace("\n","")
		res_sp = res.split("\r")
		
		best_qual = 0
		for j in res_sp:
			if "checking" in j:
				qual = j[j.index("g:")+3:j.index("%")]
				best_qual = max(float(qual), best_qual)
				
		qual_point = [i,best_qual]
		quality_list.append(qual_point)
				
	return quality_list
