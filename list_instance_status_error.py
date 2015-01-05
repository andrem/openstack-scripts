#!/usr/bin/env python
#
#
import sys
from novaclient import client
from novaclient import utils

nc = client.Client(2,
                    "<USERNAME>", 
                    "<PASSWORD>", 
                    "<ADMIN_TENANT>", 
                    "http://api.server.com:35357/v2.0")


for s in nc.servers.list(search_opts={"all_tenants": True}):
    if s.status == "ERROR":
        print "This instance %s is a %s status" % (s.name,s.status)
