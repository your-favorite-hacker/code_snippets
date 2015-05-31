#!/usr/bin/env python2
#
# ./find_ntp_nolib.py -l IPs.txt -t 500 -o ntpservers.txt
#
# simple ntp server finder by dash
# this one is not dependend on ntplib as it uses socket only and default payload
#
# [*] Found 148 entries
# [*] Entries 148 in queue
# [*] Running with 50 threads
# ==================================================
# IP
# ==================================================
# 103.x.x.x
# 157.x.x.x
#
#

import os
import sys
import Queue
import socket
import argparse
import threading

global rQ
rQ = Queue.Queue()

def openFile(hostList):
	fr = open(hostList,'r')
	rBuf = fr.readlines()
	return rBuf

def openWriteFile(outfile):
	fw = open(outfile,'wb')
	return fw

def checkNTP(host):
	payload = '\x13\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xd9\x15$\xf6Iw\x98\x00'
	# settimeout so recv is not block
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s.settimeout(3)
		s.connect((host,123))
		s.send(payload)
		rBuf = s.recv(1024)
		print '%s' % (host)
		data = '%s\n' % (host)
		rQ.put(data)
	except socket.error,e:
#		print e
		pass
	return
		
def run(args):
	""" mighty mighty function """

	if not args.thrCnt:
		thrCnt=50
	else:
		thrCnt = int(args.thrCnt)
	
	if args.outfile:
		fw = openWriteFile(args.outfile)
	
	hostList = args.hostList

	q = Queue.Queue()
	rBuf = openFile(hostList)
	print '[*] Found %d entries' % len(rBuf)
	for r in rBuf:
		r = r.rstrip('\n')
		r = r.rstrip('\r')
		q.put(r)

	print '[*] Entries %d in queue' % q.qsize()
	print '[*] Running with %d threads' % thrCnt
	print '='*50
	print 'IP'
	print '='*50
	thrList = []
	while q.qsize()>0:
		
		if len(thrList) < thrCnt:
			thrNtp = threading.Thread(target = checkNTP, args = (q.get(),))
			thrNtp.daemon = True
			thrNtp.start()
			thrList.append(thrNtp)
		
		for entry in thrList:
			if entry.isAlive()==False:
				entry.join()
				thrList.remove(entry)

		if args.outfile and rQ.qsize()>0:
			i = rQ.get()
			data = "%s" % (i)
			fw.write(data)
			fw.flush()
		else:
			if rQ.qsize()>0:
				rQ.get()

	fw.close()
	print '='*50
	print '[*] Done'
	print '='*50
	

def main():
	parser_desc = 'ntp server finder, prints found ip not using ntplib, by dash'
	prog_desc = 'find_ntp_nolib.py'
	parser = argparse.ArgumentParser(	prog = prog_desc, description = parser_desc)
	parser.add_argument("-l",action='store',required=True,help='host list with ips',dest='hostList')
	parser.add_argument('-t',action='store',required=False,help='thread count', dest='thrCnt')
	parser.add_argument('-o',action='store',required=False,help='write found data to file', dest='outfile')
	args = parser.parse_args()
	run(args)

if __name__ == "__main__":
	main()
