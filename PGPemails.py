#!/usr/bin/env python2
#
# todo
# - nicer output, ugly right now
# - interpret error 500 (too many results!!) 502 pgp mit edu is down again
# - option to download the key as well
# - socks support
#

import sys
import os
import re
import urllib2
from BeautifulSoup import BeautifulSoup


def usage():
	print "%s -- get emails of company members by pgp.mit.edu"
	print "<searchstring> <outdir>"
	print

search = sys.argv[1]
out = sys.argv[2]

if len(sys.argv)<2:
	usage()
	sys.exit(1)

try:
	os.mkdir(out)
except:
	print "dir exists %s" % out

logfile = "%s/%s.txt" % (out,out)
flog = open(logfile,"w")


search = search.rstrip("\n")
search = search.rstrip("\r")
search = urllib2.quote(search)

url = "http://pgp.mit.edu:11371/pks/lookup?search=%s&op=index" % (search)
print "Link: %s" % (url)

req = urllib2.Request(url)
req.add_header("Host","pgp.mit.edu:11371")
req.add_header("User-Agent","Internet Explorer")
req.add_header("Accept","*/*")
req.add_header("Accept-Encoding","text/html")
req.add_header("Accept-Charset","us-ascii, ISO-8859-1")
req.add_header("Accept-Language","en,*;q=0.1")
req.add_header("Referer","http://pgp.mit.edu")
req.add_header("Connection","close")

try:
	res = urllib2.urlopen(req)
except urllib2.HTTPError,e:
	print "%s" % (e)
	sys.exit(1)

data = res.read()
soup = BeautifulSoup(data)
links = soup.findAll('a')

elist = []
klist = []
for entry in links:
	elist.append(entry.contents)

for line in elist:
	line = str(line)
	if re.search('@',line):
		dline = BeautifulSoup(line,convertEntities=BeautifulSoup.HTML_ENTITIES)
		pdline = str(dline.contents)
		print pdline
