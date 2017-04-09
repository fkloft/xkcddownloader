#!/usr/bin/env python3

import re
import requests

def get_info(comic=None):
	"Gets the information about a comic."
	
	if comic is not None:
		try:
			comic = int(comic)
		except TypeError:
			raise TypeError("Comic must be an integer or None")
	
	if comic is None:
		req = requests.get("https://xkcd.com/info.0.json")
	else:
		try:
			req = requests.get("https://xkcd.com/%d/info.0.json" % comic)
		except 2:
			raise ValueError("Invalid comic ID %d" % comic)
	
	info = req.json()
	
	link = info["link"]
	
	if link.startswith("//"):
		link = "https:" + link
	
	large = None
	if link:
		if re.search("^https?://xkcd\.com/\d+[_/]large/$", link):
			content = requests.get(link)
			match = re.search('<img(?:\s+[^>]*)*\ssrc="(https?://imgs\.xkcd\.com/[^"]+)"', content.text)
			if match:
				link = match.group(1)
				if link.startswith("//"):
					link = "https:" + link
		
		if re.search("https?://(?:[a-z0-9]+\.)*xkcd.com/", link) and \
			requests.head(link, allow_redirects=True).headers["content-type"].startswith("image/"):
			large = link
	info["large"] = large
	
	return info

if __name__ == "__main__":
	#print get_info()
	for i in (
		191, 256, 273, 351, 426, 472, 482, 514, 609, 657, 681, 802, 832, 850, 851,
		871, 930, 980, 1000, 1017, 1031, 1040, 1052, 1071, 1079, 1080, 1104, 1127,
		1169, 1190, 1196, 1212, 1256, 1298, 1389, 1392, 1407, 1461, 1488, 1491, 1506,
		1509, 1525, 1551, 1572, 1688, 1723, 1799,
	):
		a=get_info(i)
		del a["transcript"]
		del a["alt"]
		del a["news"]
		import json
		print(json.dumps(a, indent=True, sort_keys=True))



