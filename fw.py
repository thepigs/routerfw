#!/usr/bin/python
import sys
import os
import telnetlib
import re
import time
os.system('python telnetenable.py 192.168.0.1 A06391D0DA9E admin password')
time.sleep(1)
def get_script_path(f):
        return os.path.dirname(os.path.realpath(sys.argv[0]))+'/'+f

fl = "WHITELIST"
if len(sys.argv)==3:
    fl=sys.argv[2]
bl=[]
set= sys.argv[1]=='set'
if set:
    print "Reading: ",get_script_path(fl)    
    for line in open(get_script_path(fl)):
        bl.append(line.strip())

tn=telnetlib.Telnet('192.168.0.1')
tn.set_debuglevel(255)
tn.read_until('#')
tn.write('iptables -F FORWARD\n')
tn.read_until('#')
tn.write('iptables -P FORWARD '+('DROP' if set else 'ACCEPT')+'\n')
tn.read_until('#')

for mac in bl:
    tn.write("iptables -A FORWARD --source "+mac+" -j ACCEPT\n");
    tn.read_until('#')
    tn.write("iptables -A FORWARD --destination "+mac+" -j ACCEPT\n");
    tn.read_until('#')
tn.close()
