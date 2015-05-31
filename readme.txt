PGPemails.py
============
script for harvesting emails of domain targets @pgp.mit.edu

find_ntp.py
===========
find ntp servers, it is a threaded script, using ntplib
as a result it prints out the ntpserver and the version running

find_ntp_nolib.py
=================
this one is not using ntplib, instead it is building up its own socket and sending a simple ntp request
to see if ntp is answering. also threaded.

generateRandomIP.sh
===================
generate random ips with nmap

