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

import HTMLParser
import threading
import urllib
import csv
import os
import sys
import thread
import time
import getopt

class parseLinks(HTMLParser.HTMLParser): 
	## @class parseLinks
	#
	#This class is for parsing html pages
	
	##The constructor
	def __init__(self): #this function is copy pasted from http://pleac.sourceforge.net/pleac_python/webautomation.html
		HTMLParser.HTMLParser.__init__(self)
		self._plaintext = "" #dont know what this is
		self._ignore = False #dont know what this is
		## @var node
		#I added this so that when crawling is happening and a new site is found, the node object being crawled can be accessed and the new site can be added in the approriate place
	
	## This function parses the tags of the website and creates new nodes for each site found.
	# The code was found from page 170 of Python Phrasebook
	#@todo add "typepad" to the list of accepable domains
	def handle_starttag(self, tag, attrs): 
		try:
			if tag == 'a': 
				for name, value in attrs:
					if name == 'href':
						if (value.find("http://")+1):
							print value
		except Exception: pass
								
opts, args = getopt.getopt(sys.argv[1:], 'd' ,['depth'])								
								
#page 170 of Python Phrasebook:
lParser = parseLinks()
try:
	s = urllib.urlopen("http://this.bigstereo.net/2011/11/02/figures/").read()
	lParser.feed(s); 
	lParser.close()
except Exception: pass

print opts, args

sys.exit(0)

