#!/usr/bin/env python3

import argparse
import io
import json
import os
import requests

from PIL import Image, ImageColor, ImageFont

import helper
import parser
import settings

config = settings.config;

if config["random"]:
	import random
	current = parser.get_info()["num"]
	config["comic"] = random.randint(1, current)

info = parser.get_info(config["comic"])

config["output"] = config["output"].replace("%title", info["title"]).replace("%comic", str(info["num"]))


if config["mode"] == 0:
	print(json.dumps(info, sort_keys=True, indent=True))

elif config["mode"] == 1:
	source = (config["large"] and info["large"]) or info["img"]
	req = requests.get(source)
	fh = open(os.path.expanduser(config["output"]), "wb")
	fh.write(req.content)
	fh.close()

elif config["mode"] == 2:
	title = info["title"]
	alt = info["alt"]
	
	if not os.path.exists(os.path.expanduser(config["font"])):
		print ("Couldn't find font file!\nPlease define path to a .ttf file!\nThe given path was: %s") % os.path.expanduser(config["font"])
		quit()
	
	if config["width"] == None or config["height"] == None:
		screen = helper.get_screen_size()
		width  = config["width"]  or screen[0] or 1024
		height = config["height"] or screen[1] or 768
	
	size = (width, height)
	
	source = (config["large"] and info["large"]) or info["img"]
	req = requests.get(source)
	comic = Image.open(io.BytesIO(req.content))
	
	wallpaper = Image.new("RGB", (width, height), ImageColor.getrgb(config["background"]))
	
	fontheight = 0
	
	if config["title"] > 0:
		if config["id"]:
			title = "%d: %s" % (info["num"], title)
		font = ImageFont.truetype(os.path.expanduser(config["font"]), config["title"])
		fontheight += helper.draw_text(font, title, width-config["left"]-config["right"])
	
	if config["desc"] > 0:
		font = ImageFont.truetype(os.path.expanduser(config["font"]), config["desc"])
		fontheight += helper.draw_text(font, alt, width-config["left"]-config["right"])
	
	maxheight = height-config["top"]-config["bottom"]-fontheight
	maxwidth = width-config["left"]-config["right"]
	
	width  = comic.size[0]
	height = comic.size[1]
	
	if config["scale"] == False:
		if width<maxwidth and height>maxheight:
			width = width*maxheight/height
			height = maxheight
		
		if height<maxheight and width>maxwidth:
			height = height*maxwidth/width
			width = maxwidth
	
	if (height>maxheight and width>maxwidth) or config["scale"] == True:
		if width/height > maxwidth/maxheight:
			height = height*maxwidth/width
			width = maxwidth
		else:
			width = width*maxheight/height
			height = maxheight
	
	width = round(width)
	height = round(height)
	
	if (width, height) != comic.size:
		comic = comic.resize((width, height), Image.ANTIALIAS)
	
	y = (maxheight-height)/2 + config["top"]
	
	if config["title"] > 0:
		font = ImageFont.truetype(os.path.expanduser(config["font"]), config["title"])
		y = helper.draw_text(font, title, size[0]-config["left"]-config["right"], wallpaper, config["left"], y, color=ImageColor.getrgb(config["fontcolor"]))
	
	wallpaper.paste(comic, (round((maxwidth-width)/2+config["left"]), round(y)))
	y += height
	
	if config["desc"] > 0:
		font = ImageFont.truetype(os.path.expanduser(config["font"]), config["desc"])
		y = helper.draw_text(font, alt, size[0]-config["left"]-config["right"], wallpaper, config["left"], y, color=ImageColor.getrgb(config["fontcolor"]))
	
	if config["attribution"]:
		helper.add_attribution(wallpaper,
			os.path.expanduser(config["font"]),
			ImageColor.getrgb(config["fontcolor"]),
			config["attributionX"],
			config["attributionY"])
	
	wallpaper.save(os.path.expanduser(config["output"]))
	
	if config["set"]:
		set_wallpaper(os.path.abspath(os.path.expanduser(config["output"])))
	
else:
	raise Exception("Invalid mode!")


