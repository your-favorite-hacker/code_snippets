#!/usr/bin/env python2
#
# ./find_ntp.py -l IPs.txt -t 500 -o ntpservers.txt
#
# simple ntp server finder by dash
#
# [*] Found 148 entries
# [*] Entries 148 in queue
# [*] Running with 50 threads
# ==================================================
# IP              Version
# ==================================================
# 103.x.x.x  2
# 157.x.x.x  3 
#
#

import os
import sys
import Queue
import ntplib
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
	c = ntplib.NTPClient()
	try:
		res = c.request(host)
		print '%s\t%d' % (host,res.version)
		data = '%s\t%d\n' % (host,res.version)
		rQ.put(data)
	except ntplib.NTPException,e:
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
	print 'IP\t\tVersion'
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
	parser_desc = 'ntp server finder, prints found ip and ntp-version, by dash'
	prog_desc = 'find_ntp.py'
	parser = argparse.ArgumentParser(	prog = prog_desc, description = parser_desc)
	parser.add_argument("-l",action='store',required=True,help='host list with ips',dest='hostList')
	parser.add_argument('-t',action='store',required=False,help='thread count', dest='thrCnt')
	parser.add_argument('-o',action='store',required=False,help='write found data to file', dest='outfile')
	args = parser.parse_args()
	run(args)

if __name__ == "__main__":
	main()
