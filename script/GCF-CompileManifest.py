#!/usr/bin/python

import json
import re

services = json.load(open('./data/GCF-Service.json'))
vms = json.load(open('./data/GCF-VM.json'))
pods = json.load(open('./data/GCF-VB.json'))

appids = {}
for pod, v in pods.items():
    for reg, v in v.items():
        for dc, v in v.items():
            for vb, v in v.items():
                for s in v["Services"]:
                    for app, nodes in services[s]['Applications'].items():
                        for node in nodes: 
                            if(node != ''): node = "-%s" % node 
                            appid = ''
                            if(re.match('^POD', s)):
                                appid = ("%s-%s-%s%s" % (s, pod, app,node))
                            elif(re.match('^REGION', s)):
                                appid = ("%s-%s-%s%s" % (s, reg, app,node))
                            elif(re.match('^DC', s)):
                                appid = ("%s-%s-%s%s" % (s, dc, app,node))
                            elif(re.match('^VB', s) or re.match('^ESX', s)):
                                appid = ("%s-%s-%s%s" % (s, vb, app,node))
                            else:
                                appid = ("%s-%s%s" % (s, app,node))
                            appids[appid] = 1

for appid, v in appids.items():
    found = False
    for region, v in vms.items():
        if appid in vms[region]:
            print "%s => %s" % (appid,vms[region][appid])
            del vms[region][appid]
            found = True
    if(not found):
        if(re.match('.+VB10', appid) or 
           re.match('.+VB11', appid) or
           'REGION_MGMT-OSAKA-VCDB-B' == appid):
            # Ignore for now 
            appid
        else:
            raise Exception("invalid appid '%s'" % appid)

for region, v in vms.items():        
    for appid, v in vms[region].items():
        if('REGION_MGMT-OSAKA-SPLF' == appid):
            appid # ignore for now
        else:
            raise Exception("unknown appid '%s'" % appid)
