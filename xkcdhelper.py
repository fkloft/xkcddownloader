#!/usr/bin/env python

import re, subprocess, Image, ImageDraw, ImageFont

def get_screen_size():
	try:
		output = subprocess.Popen(["xrandr"], stdout=subprocess.PIPE).communicate()[0]
	except OSError:
		print "Seems you aren't using Linux..."
	else:
		match = re.search("(\d+)x(\d+)\s+[0-9.]+\*", output)
		width = int(match.group(1))
		height = int(match.group(2))
		return (width, height)
	
	try:
		from win32api import GetSystemMetrics
	except ImportError:
		print "Seems you aren't using Windows..."
	else:
		width = GetSystemMetrics(0)
		height = GetSystemMetrics(1)
		return (int(width), int(height))
	
	print "Don't know, give up, size will be 1024x768"
	return (1024,768)

def draw_text(font, text, maxwidth, image=None, x=None, y=None, color=(0,0,0)):
	test = image==None or x==None or y==None;
	if test:
		image = Image.new("RGB", (maxwidth, 500))
		x = 0;
		y = 0;
	
	draw = ImageDraw.Draw(image)
	
	rest = text.split(" ")
	while len(rest):
		words = rest
		rest = []
		size = font.getsize(" ".join(words))
		width = size[0]
		while width>maxwidth and len(words)>1:
			rest.insert(0, words.pop())
			size = font.getsize(" ".join(words))
			width = size[0]
		
		if not test:
			draw.text((x+(maxwidth-width)/2,y), " ".join(words), font=font, fill=color)
		y += size[1];
	
	return y

def add_attribution(image, font, color, right=5, bottom=5):
	import os, sys
	folder = os.path.dirname(__file__)
	cc = Image.open(os.path.join(folder, "cc-by-nc.png"))
	
	text = "xkcd.com"
	font = ImageFont.truetype(font, 20)
	size = font.getsize(text)
	draw = ImageDraw.Draw(image)
	pos = [image.size[0]-size[0]-right, image.size[1]-size[1]-bottom]
	draw.text(pos, text, font=font, fill=color)
	
	pos[0] -= cc.size[0]+5
	pos[1] = image.size[1]-bottom-cc.size[1]
	image.paste(cc, tuple(pos), cc)

def set_wallpaper(filename):
	try:
		import gconf
		client = gconf.client_get_default()
		client.set_string("/desktop/gnome/background/picture_filename", filename)
	except:
		print "You can only set the wallpaper when you use GNOME!"

