#!/usr/bin/env python
#
#

import os
import sys
import argparse
import libvirt

parser = argparse.ArgumentParser(description='Hypervisor and username ssh access only.') 
parser.add_argument('-c',dest='compute')
parser.add_argument('-u',dest='username')
args = parser.parse_args()

from keystoneclient.v2_0 import client
from keystoneclient import utils
from novaclient import client as nova_client
from novaclient import utils as nova_util

def get_nova_credentials():
    d = {}
    d['username'] = os.environ['OS_USERNAME']
    d['password'] = os.environ['OS_PASSWORD']
    d['auth_url'] = os.environ['OS_AUTH_URL']
    d['auth_url_keystone'] = os.environ['OS_AUTH_URL'].replace('35357','5000') 
    d['tenant_name'] = os.environ['OS_TENANT_NAME']
    return d

if __name__ == "__main__":
    nova_credentials = get_nova_credentials()

    kc = client.Client(username=nova_credentials["username"],
        password=nova_credentials["password"], 
        tenant_name=nova_credentials["tenant_name"],
        auth_url=nova_credentials["auth_url_keystone"])

    nc = nova_client.Client(2,
        nova_credentials["username"],
        nova_credentials["password"],
        nova_credentials["tenant_name"],
        nova_credentials["auth_url"])

    """ libvirt connection using the group access """
    address =  "qemu+ssh://%s@%s/system" % (args.username,args.compute)
    conn = libvirt.openReadOnly(address)

    for domainUUID in conn.listAllDomains():
         for vm in nc.servers.list(search_opts={"all_tenants": True, 'uuid': domainUUID.UUIDString()}):
             user = utils.find_resource(kc.users, vm.user_id)
             print "%s, %s, %s, %s " % (vm.id,vm.name, user.name, user.email)
