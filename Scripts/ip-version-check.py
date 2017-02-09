#!/usr/bin/python
# A script to determine if an IPv6 IP is used in the gateway section of the user_config.yaml
# If an IPv6 IP is detected, the script will call the IPv6 validation script to validate
# the individual IP's.
## Author: James Bagwell
## Company: Nokia
## Date: 12/29/2016
import ipaddr
import yaml

def main():
    ver = 0
    ip = ''
    with open("/home/stack/user_config.yaml", "r") as stream:
        uc_data = yaml.safe_load(stream)
        ip = uc_data['CBIS']['subnets']['external']['gateway'].strip()

    ver = ipaddr.IPAddress(ip)
    print '%s is a correct IPv%s address.' % (ip, ver.version)
    if ver.version == 6:
        print "IPv6 Addresses detected in User_config.yaml"
        return True
    else:
        return False
if __name__ == "__main__":
    main()
