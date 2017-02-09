#!/usr/bin/python
## This script checks against the ntp_servers entry in the user_config.yaml, determines if it is IPv4 or IPv6 and validates those IPs
## using the inet_pton socket interface with the AF_INET family. 
## https://docs.python.org/2/library/socket.html
## Author: James Bagwell
## Company: Nokia
## Date: 01/23/2017 
import sys
import socket
import yaml
import ipaddr
from subprocess import Popen, PIPE

class CbisGlobals:
    def __init__(self): pass

    @staticmethod
    def run_process(line):
        p = Popen(line, shell=True, stdout=PIPE, stderr=PIPE)
        out, err = p.communicate()
        return out, err, p

def validate_ip_v6(ipaddress):
    try:
        socket.inet_pton(socket.AF_INET6, ipaddress)
    except socket.error:
        print("The address %s is not a valid IPv6 address" % ipaddress)
        sys.exit(1)
    return True 

def validate_ip_v4(ipaddress):
    try:
        socket.inet_pton(socket.AF_INET, ipaddress)
    except socket.error:
        print("The address %s is not a valid IPv4 Address" % ipaddress)
        sys.exit(1)
    return True

def connection_checker_dns_v4(ipaddress):
    line = "/usr/bin/nc -w 5 %s 53 < /dev/null" % ipaddress
    out, err, p = CbisGlobals.run_process(line)
    if p.returncode > 0:
        print("Port 53 for DNS address %s is not open" % ipaddress)
        sys.exit(1)

    line = "/usr/bin/dig %s" % ipaddress
    print "here in the dig section"
    out, err, p = CbisGlobals.run_process(line)
    print "the return code was %s - all good." % p.returncode
    if p.returncode > 0:
        print("Domain information groper failed against the DNS ip %s. Please correct the DNS IP" % ipaddress)
        sys.exit(1)

def connection_checker_dns_v6(ipaddress):
    line = "/usr/bin/nc -6 -w 5 %s 53 < /dev/null" % ipaddress        
    out, err, p = CbisGlobals.run_process(line)
    if p.returncode > 0:
        print("Port 53 for DNS address %s is not open" % ipaddress)
        sys.exit(1)
    line = "/usr/bin/dig %s" % ipaddress
    out, err, p = CbisGlobals.run_process(line)
    if p.returncode > 0:
        print("Domain information groper failed against the DNS ip " + ipaddress + ". Please correct the DNS IP")
        sys.exit(1)

def main():
    with open("user_config.yaml", "r") as stream:
        uc_data = yaml.load(stream)
        dns_ip = uc_data['CBIS']['common']['dns_servers']
        print(dns_ip)

        for ip in dns_ip:
            ver = ipaddr.IPAddress(ip)
            if ver.version == 6:
                validate_ip_v6(ip)
                connection_checker_dns_v6(ip) 
            else:
                validate_ip_v4(ip)
                connection_checker_dns_v4(ip)

if __name__ == "__main__":
   main()
