#!/usr/bin/python
import sys
import os
import telnetlib
import re
os.system('python telnetenable.py 192.168.0.1 A06391D0DA9E admin password')

def get_script_path(f):
        return os.path.dirname(os.path.realpath(sys.argv[0]))+'/'+f

fl = "WHITEMACS"
if len(sys.argv)==3:
    fl=sys.argv[2]
bl=[]
set= sys.argv[1]=='set'
if set:
    print "Reading: ",get_script_path(fl)    
    for line in open(get_script_path(fl)):
        m = re.match("(\\w\\w[:]\\w\\w[:]\\w\\w[:]\\w\\w[:]\\w\\w[:]\\w\\w)\\s+(\\S+)",line)
        if m:
            print "Block: ",m.group(1),m.group(2)
            bl.append([m.group(1),m.group(2)])

tn=telnetlib.Telnet('192.168.0.1')
tn.set_debuglevel(255)
tn.read_until('#')
tn.write('iptables -F FORWARD\n')
tn.read_until('#')
tn.write('iptables -P FORWARD '+('DROP' if set else 'ACCEPT')+'\n')
tn.read_until('#')

if set:
    tn.write('iptables -A FORWARD -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT\n')
    tn.read_until('#')

#iptables -A PAUSE -s 192.168.0.0/25 -j DROP
for mac in bl:
    tn.write("iptables -A FORWARD -m mac --mac-source "+mac[0]+" -j ACCEPT\n");
    tn.read_until('#')
tn.close()
