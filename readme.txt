Code Snippet Repository
***********************
Little place for putting some scripts. Nothing special, but usefull :)


PGPemails.py
------------
script for harvesting emails of domain targets @pgp.mit.edu
$ ./PGPemails.py '@openbsd.org' 10|grep 'Theo de Raadt'
[u"[u'Theo de Raadt <deraadt@openbsd.org>']"]

find_ntp.py
-----------
find ntp servers, it is a threaded script, using ntplib
as a result it prints out the ntpserver and the version running

$ ./find_ntp.py -l IPs.txt -t 500 -o ntpservers.txt

[*] Found 148 entries
[*] Entries 148 in queue
[*] Running with 50 threads
==================================================
IP              Version
==================================================
103.x.x.x  2
157.x.x.x  3 


find_ntp_nolib.py
-----------------
this one is not using ntplib, instead it is building up its own socket and sending a simple ntp request
to see if ntp is answering. also threaded.

$ ./find_ntp_nolib.py -l IPs.txt -t 500 -o ntpservers.txt

[*] Found 148 entries
[*] Entries 148 in queue
[*] Running with 50 threads
==================================================
IP
==================================================
103.x.x.x
157.x.x.x


generateRandomIP.sh
-------------------
generate random ips with nmap

find_dns.py
-----------
similar to find_ntp, but searching for dns servers. give it an ip list, generated for instance with 'generateRandomIP.sh'.

$ ./find_dns.py -l rIP.txt -t 100 -o dnsservers.txt
[*] Found 1001 entries
[*] Entries 1001 in queue
[*] Running with 100 threads
==================================================
IP          NAME
==================================================
91.x.x.x   (x.info)
191.x.x.x  (191.x.br)
67.x.x.x   (name.info)
==================================================
[*] Done

Also it has some extra options now:
find_dns.py [-h] -l HOSTLIST [-t THRCNT] [-o OUTFILE] [-n] [-d DOMAIN]

dns server finder, by dash

optional arguments:
  -h, --help   show this help message and exit
  -l HOSTLIST  host list with ips
  -t THRCNT    thread count
  -o OUTFILE   write found data to file
  -n           do not resolve ips
  -d DOMAIN    choose the domain for the dns request

If you do not like to resolve the ips via default 8.8.8.8 (google dns cluster)
choose -n. If you want to use a different domain being requested in the 
payload use -d. Default domain is: google.com

example:
./find_dns.py -l rIP.txt -t 100 -n -d microsoft.com

Author
------
dash
