#!/bin/sh
# 

if [ $# -ne 2 ];
then
	echo 'generate random ips with nmap'
	echo '<count> <outfile>'
	echo
	exit
fi

cnt=$1
outfile=$2
nmap -n -iR $cnt --exclude 127.0.0.1/8,10.0.0.0/8,172.16.0.0/12,192.168.0.0/16,224-255.-.-.- -sL | cut -d ' ' -f 5 |grep -v addresses |grep -v nmap  > $outfile

