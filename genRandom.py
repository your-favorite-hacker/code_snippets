#!/usr/bin/env python2
#
# important part ripped off shamelessly here:
# http://www.codingwithcody.com/2010/05/generate-random-ip-with-python/
#

import os
import sys
from random import randrange

def usage():
	print 'random ip generator in python'
	print 'august 2015, dash'
	print '<ip cnt>'
	print

def generateIP():
    blockOne = randrange(0, 255, 1)
    blockTwo = randrange(0, 255, 1)
    blockThree = randrange(0, 255, 1)
    blockFour = randrange(0, 255, 1)
    if blockOne == 10:
        return generateIP()
    elif blockOne == 172:
        return generateIP()
    elif blockOne == 192:
        return generateIP()
    else:
		print str(blockOne) + '.' + str(blockTwo) + '.' + str(blockThree) + '.' + str(blockFour)

if len(sys.argv)<2:
	usage()
	exit()

ipcnt = int(sys.argv[1])
 
i=0
while i!=ipcnt:
	generateIP()
	i+=1
