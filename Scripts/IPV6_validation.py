#!/usr/bin/python
## A simple validation script that grabs the relebant Ipv6 addresses in
## user_config.yaml and validates them using the inet_pton socket interface
## with the AF_INET6 family. 
## https://docs.python.org/2/library/socket.html
## Author: James Bagwell
## Company: Nokia
## Date: 12/29/2016 
import os
import sys
import socket
import yaml
import ipaddr

class V6List:
    def __init__(self):
        self.v6list = []

    def validate_ip(self):
        for ip_addr in self.v6list:
            try:
                socket.inet_pton(socket.AF_INET6, ip_addr)
            except socket.error:
                print("The address %s is not a valid IP address" % ip_addr)
                sys.exit(1)
        return True 

    def append_ip(self, ipaddress):
        self.v6list.append(ipaddress)
    
def main():
    ver = 0
    ip = ''
    with open("/home/stack/user_config.yaml", "r") as stream:
        uc_data = yaml.safe_load(stream)
        ip = uc_data['CBIS']['subnets']['external']['gateway'].strip()
    ver = ipaddr.IPAddress(ip)
    list_vers = ver.version
    if list_vers == 6:
        with open("/home/stack/user_config.yaml", "r") as stream:
            uc_data = yaml.safe_load(stream)
            list_obj = V6List()
            list_obj.append_ip(uc_data['CBIS']['subnets']['external']['gateway'])
            list_obj.append_ip(uc_data['CBIS']['subnets']['external']['ip_range_start'])
            list_obj.append_ip(uc_data['CBIS']['subnets']['external']['ip_range_end'])
        list_obj.validate_ip()
        

if __name__ == "__main__":
   main()
