#!/usr/bin/env python

import urllib2, HTMLParser, re

def get_info(comic=None):
	"Gets the information about a comic."
	
	if comic is not None:
		try:
			comic = int(comic)
		except TypeError:
			raise TypeError("Comic must be an integer or None")
	
	parser = HTMLParser.HTMLParser()
	def unescape(string):
		string = parser.unescape(string.decode("utf-8"))
		return string
	
	if comic is None:
		req = urllib2.urlopen("http://xkcd.com/")
	else:
		try:
			req = urllib2.urlopen("http://xkcd.com/%d"%comic)
		except urllib2.HTTPError:
			raise ValueError("Invalid comic ID % 2d" % comic)
	
	line = req.readline()
	while not ' id="middleContent"' in line:
		line = req.readline()
	
	while not '<h1>' in line:
		line = req.readline()
	
	match = re.search('<h1>([^<]+)<\/h1>', line)
	title = unescape(match.group(1))
	
	while not '<img ' in line:
		line = req.readline()
	
	match = re.search('src="([^"]+)"', line)
	src = match.group(1)
	
	match = re.search('title="([^"]+)"', line)
	desc = unescape(match.group(1))
	
	if comic is None:
		while not 'Permanent link' in line:
			line = req.readline()
		
		match = re.search('http://xkcd.com/(\d+)/', line)
		comic = int(match.group(1))
	
	req.close()
	return \
	{
		"comic": comic,
		"title": title,
		"image": src,
		"desc":  desc
	}

if __name__ == "__main__":
	print get_info()

