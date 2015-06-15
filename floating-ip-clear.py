#!/usr/bin/python
#
#

import os
import sys
from neutronclient.v2_0 import client as neutronclient
from optparse import OptionParser

def get_nova_credentials(user,password,auth,tenant):
    d = {}
    d['username'] = user
    d['password'] = password
    d['auth_url'] = auth
    d['tenant_name'] = tenant
    return d

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-u", "--os-username", dest="os_username", help="OS_USERNAME")
    parser.add_option("-p", "--os-password", dest="os_password", help="OS_PASSWORD")
    parser.add_option("-a", "--os-auth-url", dest="os_auth_url", help="OS_AUTH_URL")
    parser.add_option("-t", "--os-tenant-name", dest="os_tenant_name", help="OS_TENANT_NAME")
    (options, args) = parser.parse_args()


    if ( not options.os_username) or (not options.os_password) or (not options.os_auth_url) or (not options.os_tenant_name): 
        parser.print_help() 
        sys.exit(1)

    nova_credentials = get_nova_credentials(options.os_username, options.os_password, options.os_auth_url, options.os_tenant_name)

    neutron = neutronclient.Client(auth_url=nova_credentials["auth_url"],
        username=nova_credentials["username"],
        password=nova_credentials["password"],
        tenant_name=nova_credentials["tenant_name"])
   
  
    floatingips = neutron.list_floatingips()

    for floatingip in floatingips['floatingips']:
        if not floatingip['fixed_ip_address']:
            print "Deleting %s %s" % (floatingip['id'], floatingip['floating_ip_address'])
            neutron.delete_floatingip(floatingip['id'])

