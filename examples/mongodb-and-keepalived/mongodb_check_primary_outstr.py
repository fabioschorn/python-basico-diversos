#!/usr/bin/env python
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import sys
import netifaces as ni

client = MongoClient('mongodb://127.0.0.1:27017')
# compare the hostname and port of the primary with the local host and port
try:
    if client.admin.command("isMaster")['primary'] == ni.ifaddresses('ens192')[2][0]['addr'] + ':27017':
        print ("Primary")
    else:
        print ("Secondary")
except ConnectionFailure:
    print ("Connection Failure")
    sys.exit(1)