#!/usr/bin/env python
#
#

import os
import sys

from keystoneclient.v2_0 import client
from keystoneclient import utils
import glanceclient

kc = client.Client(username=os.environ['OS_USERNAME'],
    password=os.environ['OS_PASSWORD'],
    tenant_name=os.environ['OS_TENANT_NAME'],
    auth_url=os.environ['OS_AUTH_URL'].replace('35357','5000'))

glance = glanceclient.Client(1,"ENDPOINT-URL", token=kc.auth_token)

for image in glance.images.list():
    print image
