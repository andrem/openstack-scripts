#!/usr/bin/python
#
#

import os
from neutronclient.v2_0 import client as neutronclient

def get_nova_credentials():
    d = {}
    d['username'] = os.environ['OS_USERNAME']
    d['password'] = os.environ['OS_PASSWORD']
    d['auth_url'] = os.environ['OS_AUTH_URL']
    d['tenant_name'] = os.environ['OS_TENANT_NAME']
    return d

nova_credentials = get_nova_credentials()

neutron = neutronclient.Client(auth_url=nova_credentials["auth_url"],
    username=nova_credentials["username"],
    password=nova_credentials["password"],
    tenant_name=nova_credentials["tenant_name"])

agents = neutron.list_agents()

for agent in agents['agents']:
    if agent["alive"] == False:
        print "[%s]: %s is down" % (agent["host"], agent["binary"])

