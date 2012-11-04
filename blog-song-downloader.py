#!/usr/bin/python
# 
# Copyright 2010 Daniel Snider
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

""" Description: This script downloads all the music download links on a webpage if the downloads are direct .mp3 links. Downloads run in serial.
	Usage: Call command from command line with a fully qaulified URL as the only argument.
"""

import sys
import httplib
import getopt
from urlparse import urlparse

#cleans the URL a bit
def urlparse(url):
	split = url.partition(".com")
	return split[0].strip("http://") + split[1], split[2]
	
#uses the ending of the url as the song name	
def songnameparse(url):
	start = url.rfind("/") + 1
	end = len(url)
	songname = ""
	for c in range(end - start):
		songname =  songname + url[c + start]
	return songname

#get arg and clean it, assuming it's a url
opts, args = getopt.getopt(sys.argv[1:], '' ,[''])			
domain, directory = urlparse(args[0])
print "domain", domain, "directory", directory

#download the webpage of the url
conn = httplib.HTTPConnection(domain, 80, timeout = 2000) #connect to the site
conn.request("GET", directory) #send GET
r1 = conn.getresponse() #read response
page =  r1.read()

print "starting"

#for every mp3 link found print the link in html format
for line in page.split("\n"):
	if "href" in line:
		if ".mp3" in line:
			if "http" in line: 
				try:	#lots of random shit can happen, lets avoid that				
					songURL = ""
					end = line.find(".mp3")
					start = line.find("http") 
					for c in range(end - start + 4):
						songURL =  songURL + line[c + start]
					print songURL
					print songnameparse(songURL)
					conn = httplib.HTTPConnection(urlparse(songURL)[0], 80, timeout = 2000) #connect to the site
					conn.request("GET", urlparse(songURL)[1]) #send GET
					r1 = conn.getresponse() #read response
					song =  r1.read()
					f = open(songnameparse(songURL), 'w')
					f.write(song)
					f.close()
				except: all			
print "leaving"
sys.exit(0)
