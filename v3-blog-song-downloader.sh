#!/bin/bash
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

"""	This program downloads mp3 song links from a website
	Inputs: url of website with .mp3s, output path for files
"""

url=$1  
html_file="page.html"
of=$2
count=1

if ! test $1 #exit if no param
then
	echo "Usage error: You did not supply a url as a parameter"
	exit 1
fi

if ! test $2 #exit if no param
then
	echo "You specified a path. Make sure it ends with a \"/\"."
	of="./"
fi

if test $? -ne 0
then
	echo "Website error: You did not supply a correct url"
	exit 2
fi
if test $? -ne 0
then
	echo "Website error: You did not supply a correct url"
	exit 2
fi

grep "href" $html_file | grep "\.mp3" > ./links.txt

if test $? -ne 0
then
	echo "Error: There are no mp3s"
	exit 3
fi

if test $1 == "-h"
then
	echo "Usage: $0 [URL] [SAVE LOCATION/]"
	exit 4
fi

if test $2 == "-d"
then
	of="/usr/local/www/media/"
fi

wget -U "dan's fun script" -q -O $html_file $1 #download webpage

#extract info
grep ">.*</a>" -o ./links.txt > ./song_names.txt
grep href=\'.*\' -o ./links.txt > ./song_links.txt

#remove extra chars used by grep search
sed  "s=<\/a>==g" song_names.txt | sed "s/>//g" > ./song_names2.txt
sed s/\'//g song_links.txt | sed "s/href=//g" > ./song_links2.txt

echo "-------- Found `wc -l links.txt | cut -d ' ' -f 1` links. :) --------"
while read name
do
	link=`sed -n -e "$count"p -e "$count"q song_links2.txt`
	name=`echo $name | sed s/' '/'_'/g`
	name="$name".mp3
	echo "DLing: $name from $link to $of"
	wget -U "dan's fun script" -q -O $of"$name" $link
	count=$(($count+1))
done <song_names2.txt
exit 0