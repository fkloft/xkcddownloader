#!/usr/bin/env python

import argparse, Image, ImageColor, ImageDraw, ImageFont, os, tempfile, urllib2, xkcdparser, xkcdsettings
from xkcdhelper import *

arguments = xkcdsettings.arguments;

if arguments["random"]:
	import random
	current = xkcdparser.get_info(None)["comic"]
	arguments["comic"] = random.randint(1,current)

info = xkcdparser.get_info(arguments["comic"])

arguments["output"] = arguments["output"].replace("%title", info["title"]).replace("%comic", str(info["comic"]))


if arguments["mode"] == 0:
	print "Comic:\n%d\nTitle:\n%s\nDescription:\n%s\nImage:\n%s" % \
	      (info["comic"], info["title"], info["desc"], info["image"])

elif arguments["mode"] == 1:
	req = urllib2.urlopen(info["image"])
	fh = open(os.path.expanduser(arguments["output"]), "wb")
	fh.write(req.read())
	fh.close()
	req.close()

elif arguments["mode"] == 2:
	title = info["title"]
	desc  = info["desc"]
	
	if not os.path.exists(os.path.expanduser(arguments["font"])):
		print "Couldn't find font file!\nPlease define path to a .ttf file!\nThe given path was: %s" % os.path.expanduser(arguments["font"])
		quit()
	
	if arguments["width"]==None or arguments["height"]==None:
		screen = get_screen_size()
		width  = arguments["width"]  or screen[0] or 1024
		height = arguments["height"] or screen[1] or 768
	
	size = (width, height)
	
	req = urllib2.urlopen(info["image"])
	fh = tempfile.NamedTemporaryFile(mode='wb', suffix='png', delete=False)
	tempname = fh.name
	fh.write(req.read())
	fh.close()
	req.close()
	
	comic = Image.open(os.path.expanduser(tempname))
	wallpaper = Image.new("RGB", (width, height), ImageColor.getrgb(arguments["background"]))
	
	fontheight = 0
	
	if arguments["title"] > 0:
		font = ImageFont.truetype(os.path.expanduser(arguments["font"]), arguments["title"])
		fontheight += draw_text(font, title, width-arguments["left"]-arguments["right"])
	
	if arguments["desc"] > 0:
		font = ImageFont.truetype(os.path.expanduser(arguments["font"]), arguments["desc"])
		fontheight += draw_text(font, desc, width-arguments["left"]-arguments["right"])
	
	maxheight = height-arguments["top"]-arguments["bottom"]-fontheight
	maxwidth = width-arguments["left"]-arguments["right"]
	
	width  = comic.size[0]
	height = comic.size[1]
	
	if arguments["scale"] == False:
		if width<maxwidth and height>maxheight:
			width = width*maxheight/height
			height = maxheight
		
		if height<maxheight and width>maxwidth:
			height = height*maxwidth/width
			width = maxwidth
	
	if (height>maxheight and width>maxwidth) or arguments["scale"] == True:
		if width/height > maxwidth/maxheight:
			height = height*maxwidth/width
			width = maxwidth
		else:
			width = width*maxheight/height
			height = maxheight
	
	if (width, height) != comic.size:
		comic = comic.resize((width, height), Image.ANTIALIAS)
	
	y = (maxheight-height)/2 + arguments["top"]
	
	if arguments["title"] > 0:
		font = ImageFont.truetype(os.path.expanduser(arguments["font"]), arguments["title"])
		y = draw_text(font, title, size[0]-arguments["left"]-arguments["right"], wallpaper, arguments["left"], y, color=ImageColor.getrgb(arguments["fontcolor"]))
	
	wallpaper.paste(comic, ((maxwidth-width)/2+arguments["left"], y))
	y += height
	
	if arguments["desc"] > 0:
		font = ImageFont.truetype(os.path.expanduser(arguments["font"]), arguments["desc"])
		y = draw_text(font, desc, size[0]-arguments["left"]-arguments["right"], wallpaper, arguments["left"], y, color=ImageColor.getrgb(arguments["fontcolor"]))
	
	if arguments["attribution"]:
		add_attribution(wallpaper,
		                os.path.expanduser(arguments["font"]),
		                ImageColor.getrgb(arguments["fontcolor"]),
		                arguments["attributionX"],
		                arguments["attributionY"])
	
	wallpaper.save(os.path.expanduser(arguments["output"]))
	
	if arguments["set"]:
		set_wallpaper(os.path.abspath(os.path.expanduser(arguments["output"])))
	
else:
	raise Exception("Invalid mode!")


