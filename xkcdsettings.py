#!/usr/bin/env python

import os, json, argparse

folder = os.path.dirname(__file__)

default = \
{
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
	
	# scale comic to image size, even if it is smaller
	"scale": False,
	
	# set as desktop wallpaper
	"set": False
}

def merge_config(config={}):
	new = default.copy()
	
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
	
	for i in ("top", "bottom", "left", "right", "title", "desc"):
		try:
			value = int(config[i])
			if value >= 0:
				new[i] = value
		except:
			pass
	
	for i in ("random", "scale", "set"):
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

config_file = "$HOME/.xkcddownloader-dev"
try:
	import win32api
except ImportError:
	pass
else:
	config_file = "%appdata%\\xkcddownloader-dev"

try:
	fh = file(os.path.expandvars(config_file))
	config = json.load(fh)
	config = merge_config(config)
except:
	print "couldn't load configuration file, using defaults"
	config = default


parser = argparse.ArgumentParser(description='Downloads images from xkcd and make wallpapers out of them.',
                                 epilog=('All options can be defined in the configuration file %s. '+
                                        'Command line options override configuration file options. '+
                                        'See %s for an example file.') % (config_file, os.path.join(os.path.dirname(__file__),"config.example")))
parser.add_argument('-i', '--info',
                   dest='mode', action='store_const', const=0, default=config["mode"],
                   help='Download nothing, only show details of the comic'+(config["mode"]==0 and " (default)" or ""))
parser.add_argument('-d', '--download',
                   dest='mode', action='store_const', const=1, default=config["mode"],
                   help='Download the image without editing it'+(config["mode"]==1 and " (default)" or ""))
parser.add_argument('-w', '--wallpaper',
                   dest='mode', action='store_const', const=2, default=config["mode"],
                   help='Download the image and make a wallpaper out of it'+(config["mode"]==2 and " (default)" or ""))
parser.add_argument('-c', '--comic',
                   action='store', default=config["comic"], type=int, metavar="NUM",
                   help='Select the comic by its ID (default: %s)' % (config["comic"]==None and "current" or config["comic"]))
parser.add_argument('-q', '--random',
                   action='store_const', const=True, default=config["random"],
                   help='Use a random comic (and ignore -c)')
parser.add_argument('-Q', '--norandom', dest="random",
                   action='store_const', const=False, default=config["random"],
                   help='Don\'t use a random comic (useful to override config file)')
parser.add_argument('-o', '--output',
                   action='store', default=config["output"], type=str, metavar="FILE",
                   help='Specify the output file when downloading an image or making a wallpaper.\n\
                         %%%%comic is replaced by the number of the comic, %%%%title likewise. (default: %s)' % config["output"])
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
parser.add_argument('-u', '--scale',
                   action='store_const', const=True, default=config["scale"],
                   help='Upscale the image if it is smaller than the available space')
parser.add_argument('-U', '--noscale', dest="scale",
                   action='store_const', const=False, default=config["scale"],
                   help='Don\'t scale the image if it is smaller than the available space (useful to override config file)')
parser.add_argument('-s', '--set',
                   action='store_const', const=True, default=config["set"],
                   help='Set as desktop wallpaper (GNOME only)')
parser.add_argument('-S', '--noset', dest="set",
                   action='store_const', const=False, default=config["set"],
                   help='Don\'t set as desktop wallpaper (useful to override config file)')
args = parser.parse_args()

arguments = dict([(i, getattr(args, i)) for i in default.keys()])


