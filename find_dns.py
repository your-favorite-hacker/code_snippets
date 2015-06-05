#!/usr/bin/env python2
#
# ./find_dns.py -l IPs.txt -t 500 -o dnsservers.txt
#
# simple dns server finder by dash
#
#./find_dns.py -l rIP.txt -t 100 
#[*] Found 1001 entries
#[*] Entries 1001 in queue
#[*] Running with 100 threads
#==================================================
#IP          NAME
#==================================================
#91.x.x.x   (x.info)
#191.x.x.x  (191.x.br)
#67.x.x.x   (name.info)
#==================================================
#[*] Done
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

def checkDNS(host):
	payload = 'J\x8e\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x03hotmail\x02de\x00\x00\x01\x00\x01'
	# settimeout so recv is not block
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s.settimeout(3)
		s.connect((host,53))
		s.send(payload)
		rBuf = s.recv(1024)
		name = ''
		try:
			name = socket.gethostbyaddr(host)[0]
		except socket.herror,e:
			pass
		if name == '':
			print '%s' % (host)
			data = '%s\n' % (host)
		else:
			print '%s\t(%s)' % (host,name)
			data = '%s\t(%s)\n' % (host,name)
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
	print 'IP\t\tNAME'
	print '='*50
	thrList = []
	while q.qsize()>0:
		
		if len(thrList) < thrCnt:
			thrDns = threading.Thread(target = checkDNS, args = (q.get(),))
			thrDns.daemon = True
			thrDns.start()
			thrList.append(thrDns)
		
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

	if args.outfile:
		fw.close()
	print '='*50
	print '[*] Done'
	print '='*50
	

def main():
	parser_desc = 'dns server finder, by dash'
	prog_desc = 'find_dns.py'
	parser = argparse.ArgumentParser(	prog = prog_desc, description = parser_desc)
	parser.add_argument("-l",action='store',required=True,help='host list with ips',dest='hostList')
	parser.add_argument('-t',action='store',required=False,help='thread count', dest='thrCnt')
	parser.add_argument('-o',action='store',required=False,help='write found data to file', dest='outfile')
	args = parser.parse_args()
	run(args)

if __name__ == "__main__":
	main()
