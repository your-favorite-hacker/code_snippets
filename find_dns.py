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
import time
import Queue
import struct
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

def parseDomain(domain):
	do = domain.split('.')
	if len(do) != 2:
		print '[!] Sorry, unknown domain type: %s\nExample:google.com' % (domain)
		return False
	tld = do[1]
	tld_len = struct.pack('>B', len(tld))
	tld_sub = do[0]
	tld_sub_len = struct.pack('>B', len(tld_sub))
	dom_pay = '%c%s%c%s' % (tld_sub_len,tld_sub,tld_len,tld)
	return dom_pay
	
	

def checkDNS(payload,host,resolv,debug):
	# settimeout so recv is not block
	rBuf_len = -1
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s.settimeout(5)
		s.connect((host,53))
		s.send(payload)
		rBuf = s.recv(1024)
		rBuf_len = len(rBuf)
		name = ''
		# default we resolve IPs as long as -n is not choosen
		if resolv:
			try:
				name = socket.gethostbyaddr(host)[0]
			except socket.herror,e:
				pass

		if name == '':
			if debug:
				print '%s\t%d\t%s' % (host,rBuf_len,repr(rBuf))
				data = '%s%d\t%s\n' % (host,rBuf_len,repr(rBuf))
			else:
				print '%s\t%d' % (host,rBuf_len)
				data = '%s%d\n' % (host,rBuf_len)
		else:
			if debug:
				print '%s\t(%s) %d\t%s' % (host,name,rBuf_len,repr(rBuf))
				data = '%s\t(%s) %d\t%s\n' % (host,name,rBuf_len,repr(rBuf))
			else:
				print '%s\t(%s) %d' % (host,name,rBuf_len)
				data = '%s\t(%s) %d\n' % (host,name,rBuf_len)

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

	dom_pay = parseDomain(args.domain)
	payload = 'J\x8e\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00%s\x00\x00\x01\x00\x01' % (dom_pay)
	
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
	if args.resolv:
		print 'IP\t\tNAME\tPaylen'
	else:
		print 'IP\t\tPaylen'

	print '='*50
	thrList = []
	while True:
	#while q.qsize()>0:
		
		if len(thrList) < thrCnt and q.qsize()>0:
			thrDns = threading.Thread(target = checkDNS, args = (payload,q.get(),args.resolv,args.debug))
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

		if q.qsize()==0 and len(thrList) == 0:
			break
	
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
	parser.add_argument('-n',action='store_false',default=True,required=False,help='do not resolve ips', dest='resolv')
	parser.add_argument('-d',action='store',default='google.com',required=False,help='choose the domain for the dns request', dest='domain')
	parser.add_argument('--debug',action='store_true',default=False,required=False,help='debug output', dest='debug')
	args = parser.parse_args()
	run(args)

if __name__ == "__main__":
	main()
