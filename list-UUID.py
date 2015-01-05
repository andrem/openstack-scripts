#!/usr/bin/env python
#
#
import libvirt
import sys
from novaclient import client
from novaclient import utils

nc = client.Client(2,
                    "<USERNAME>", 
                    "<PASSWORD>", 
                    "<PROJECT_ID>", 
                    "http://server.com:35357/v2.0")


for h in nc.hypervisors.list():
    address =  "qemu+ssh://<USERNAME>@%s/system" % h.host_ip
    conn = libvirt.openReadOnly(address)
    domains = conn.listAllDomains()

    for domainUUID in domains:
        print "%s : %s " % (h.hypervisor_hostname,domainUUID.UUIDString()) 
