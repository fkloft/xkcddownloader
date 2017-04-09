#!/usr/bin/env python

import os, json, argparse

folder = os.path.dirname(__file__)
config_file = "$HOME/.xkcddownloader"
try:
	import win32api
except ImportError:
	pass
else:
	config_file = "%appdata%\\xkcddownloader"

default = \
{
	# config file
	# (the only option that can't be set in the config file :-)
	"config": config_file,
	
	# 0: print details
	# 1: download image
	# 2: download image and make a wallpaper from it
	"mode": 2,
	
	# number of comic to use or None for current
	"comic": None,
	
	# choose a random comic (and ignore "comic")
	"random": False,
	
	# where to save the file
	"output": "~/xkcd.png",
	
	# Size of the wallpaper. Use None to use screen size
	"width": None,
	"height": None,
	
	# padding
	"top":    30,
	"bottom": 30,
	"left":   50,
	"right":  50,
	
	# colors and font
	"background": "white",
	"fontcolor": "black",
	"font": os.path.join(folder, "xkcd.ttf"),
	"title": 35,
	"desc": 25,
	
	# show ID in title
	"id": False,
	
	# scale comic to image size, even if it is smaller
	"scale": False,
	
	# use large version of the comic
	"large": True,
	
	# set as desktop wallpaper
	"set": False,
	
	# attribution
	"attribution": True,
	# padding
	"attributionX": 5,
	"attributionY": 25
}

def merge_config(config={}, base=None):
	new = (base or default).copy()
	
	try:
		value = int(config["mode"])
		if value<=2 and value >=0:
			new["mode"] = value
	except:
		pass
	
	for i in ("comic", "width", "height"):
		try:
			value = config[i]
			if(value is None):
				new[i] = None
			elif int(value) > 0:
				new[i] = int(value)
		except:
			pass
	
	for i in ("top", "bottom", "left", "right", "title", "desc", "attributionX", "attributionY"):
		try:
			value = int(config[i])
			if value >= 0:
				new[i] = value
		except:
			pass
	
	for i in ("id", "random", "scale", "set", "attribution", "large"):
		try:
			if i in config:
				new[i] = bool(config[i])
		except:
			pass
	
	for i in ("output", "background", "fontcolor", "font"):
		try:
			if i in config:
				new[i] = str(config[i])
		except:
			pass
	
	return new

def parse_args(config):
	parser = argparse.ArgumentParser(description='Downloads images from xkcd and make wallpapers out of them.',
	                                 epilog=('All options (except -C) can be defined in the configuration file %s. '+
	                                        'Command line options override configuration file options. '+
	                                        'See %s for an example file.') % (config_file, os.path.join(os.path.dirname(__file__),"config.example")))
	parser.add_argument('-C', '--config',
	                    action='store', default=config["config"], metavar="FILE",
	                    help='Use a custom config file (default: %s)' % os.path.expandvars(config["config"]))
	switch = parser.add_mutually_exclusive_group()
	switch.add_argument('-i', '--info',
	                    dest='mode', action='store_const', const=0, default=config["mode"],
	                    help='Download nothing, only show details of the comic'+(config["mode"]==0 and " (default)" or ""))
	switch.add_argument('-d', '--download',
	                    dest='mode', action='store_const', const=1, default=config["mode"],
	                    help='Download the image without editing it'+(config["mode"]==1 and " (default)" or ""))
	switch.add_argument('-w', '--wallpaper',
	                    dest='mode', action='store_const', const=2, default=config["mode"],
	                    help='Download the image and make a wallpaper out of it'+(config["mode"]==2 and " (default)" or ""))
	parser.add_argument('-c', '--comic',
	                    action='store', default=config["comic"], type=int, metavar="NUM",
	                    help='Select the comic by its ID (default: %s)' % (config["comic"]==None and "current" or config["comic"]))
	random = parser.add_mutually_exclusive_group()
	random.add_argument('-q', '--random',
	                    action='store_const', const=True, default=config["random"],
	                    help='Use a random comic (and ignore -c)')
	random.add_argument('-Q', '--norandom', dest="random",
	                    action='store_const', const=False, default=config["random"],
	                    help='Don\'t use a random comic (useful to override config file)')
	parser.add_argument('-o', '--output',
	                    action='store', default=config["output"], type=str, metavar="FILE",
	                    help='Specify the output file when downloading an image or making a wallpaper.\n\
	                          %%%%comic is replaced by the number of the comic, %%%%title likewise. (default: %s)' % config["output"])
	scale  = parser.add_mutually_exclusive_group()
	scale .add_argument('-u', '--scale',
	                    action='store_const', const=True, default=config["scale"],
	                    help='Upscale the image if it is smaller than the available space')
	scale .add_argument('-U', '--noscale', dest="scale",
	                    action='store_const', const=False, default=config["scale"],
	                    help='Don\'t scale the image if it is smaller than the available space (useful to override config file)')
	large  = parser.add_mutually_exclusive_group()
	large .add_argument('-m', '--large',
	                    action='store_const', const=True, default=config["large"],
	                    help='Use the large version of the comic. This works only with some special comics (e.g. 657)'+(config["large"] and " (default)" or ""))
	large .add_argument('-M', '--nolarge', dest="large",
	                    action='store_const', const=False, default=config["large"],
	                    help='Don\'t use the large image (useful to override config file)'+(config["large"]==False and " (default)" or ""))
	parser.add_argument('-x', '--width',
	                    action='store', default=config["width"], type=int, metavar="NUM",
	                    help='Specify the width when making a wallpaper (default: %s)'%(config["width"]==None and "use current screen resolution" or config["width"]))
	parser.add_argument('-y', '--height',
	                    action='store', default=config["height"], type=int, metavar="NUM",
	                    help='Specify the height when making a wallpaper (default: %s)'%(config["height"]==None and "use current screen resolution" or config["height"]))
	parser.add_argument('-g', '--background',
	                    action='store', default=config["background"], type=str, metavar="COLOR",
	                    help='Specify the background color (HTML/CSS notations). Default is "%s"' % config["background"])
	parser.add_argument('-f', '--fontcolor',
	                    action='store', default=config["fontcolor"], type=str, metavar="COLOR",
	                    help='Specify the background color (HTML/CSS notations). Default is "%s"' % config["fontcolor"])
	parser.add_argument('-F', '--font',
	                    action='store', default=config["font"], type=str, metavar="FILE",
	                    help='Specify the font for the title and the description (defaults to %s)' % config["font"])
	titleid = parser.add_mutually_exclusive_group()
	titleid.add_argument('-n', '--withid', dest="id",
	                    action='store_const', const=True, default=config["id"],
	                    help='Display the comid ID in the title'+(config["id"] and " (default)" or ""))
	titleid.add_argument('-N', '--noid', dest="id",
	                    action='store_const', const=False, default=config["id"],
	                    help='Don\'t display the comic ID'+(config["id"]==False and " (default)" or ""))
	parser.add_argument('-T', '--title',
	                    action='store', default=config["title"], type=int, metavar="NUM",
	                    help='Specify the font size of the title (use 0 to not show the title). Default is %s' % config["title"])
	parser.add_argument('-D', '--desc',
	                    action='store', default=config["desc"], type=int, metavar="NUM",
	                    help='Specify the font size of the description (use 0 to not show the description). Default is %s' % config["desc"])
	parser.add_argument('-t', '--top',
	                    action='store', default=config["top"], type=int, metavar="NUM",
	                    help='Padding on the top side of the wallpaper. Default is %s' % config["left"])
	parser.add_argument('-b', '--bottom',
	                    action='store', default=config["bottom"], type=int, metavar="NUM",
	                    help='Padding on the bottom side of the wallpaper. Default is %s' % config["bottom"])
	parser.add_argument('-l', '--left',
	                    action='store', default=config["left"], type=int, metavar="NUM",
	                    help='Padding on the left side of the wallpaper. Default is %s' % config["left"])
	parser.add_argument('-r', '--right',
	                    action='store', default=config["right"], type=int, metavar="NUM",
	                    help='Padding on the right side of the wallpaper. Default is %s' % config["right"])
	attrib = parser.add_mutually_exclusive_group()
	attrib.add_argument('-a', '--attribution',
	                    action='store_const', const=True, default=config["attribution"],
	                    help='Add CC-BY-NC attribution in the wallpaper (Do this if you want to distribute the wallpaper)')
	attrib.add_argument('-A', '--noattribution', dest="attribution",
	                    action='store_const', const=False, default=config["attribution"],
	                    help='Don\'t add attribution (useful to override config file)')
	parser.add_argument('-X', '--attributionX',
	                    action='store', default=config["attributionX"], type=int, metavar="NUM",
	                    help='Padding between attribution and right edge. Default is %s' % config["attributionX"])
	parser.add_argument('-Y', '--attributionY',
	                    action='store', default=config["attributionY"], type=int, metavar="NUM",
	                    help='Padding between attribution and bottom edge. Default is %s' % config["attributionY"])
	desktop = parser.add_mutually_exclusive_group()
	desktop.add_argument('-s', '--set',
	                    action='store_const', const=True, default=config["set"],
	                    help='Set as desktop wallpaper (GNOME only)')
	desktop.add_argument('-S', '--noset', dest="set",
	                    action='store_const', const=False, default=config["set"],
	                    help='Don\'t set as desktop wallpaper (useful to override config file)')
	args = parser.parse_args()
	
	new = dict([(i, getattr(args, i)) for i in default.keys()])
	return new

try:
	fh = file(os.path.expandvars(config_file))
	config = json.load(fh)
	config = merge_config(config)
except:
	print "couldn't load default configuration file, using default values"
	config = default

arguments = parse_args(config)

if arguments["config"] != default["config"]:
	try:
		fh = file(os.path.expandvars(arguments["config"]))
		custom = json.load(fh)
		custom = merge_config(custom)
	except:
		print "couldn't load given configuration file, using defaults"
		custom = config
	else:
		arguments = parse_args(custom)
else:
	custom = config

