#!/usr/bin/python
import requests
import json
import random
import sys

if len(sys.argv) < 2:
    print "usage: {} <count> [collid file]".format(sys.argv[0])
    exit(1)

wanted = int(sys.argv[1])

if len(sys.argv)  == 3:
    f=open(sys.argv[2])
else:
    f=sys.stdin

url_template='http://cnx.org/content/{}/latest/?collection={}/latest'
cids=f.read().split()
f.close()
urls = []
for c in cids:
    r=requests.get('http://cnx.org/content/%s/latest/containedModuleIds' % c)
    mids=json.loads(r.content.replace("'",'"'))
    for m in mids:
        urls.append(url_template.format(m,c))

count = min(wanted,len(urls))
r_urls=random.sample(urls,count)
print('\n'.join(r_urls))
