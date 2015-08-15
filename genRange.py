#!/usr/bin/env python2
#
#simple range generator
#august 2015, dash

import os
import sys
import struct
import socket
import netaddr

def usage():
	print 'generate ip list from range'
	print '<startip> <endip>'
	print 'example: ./%s 1.1.1.1 1.1.1.255'
	print

if len(sys.argv)<3:
	usage()
	exit()

s = sys.argv[1]
e = sys.argv[2]

i=netaddr.IPRange(s,e)
ss = i.first
se = i.last

o=0
res = se-ss
while o != res + 1:
	conv_ip = ss + o
	print socket.inet_ntoa(struct.pack('!L', conv_ip))
	o+=1
