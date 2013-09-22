import sys
import json
import re
import csv

appids = {}
with open('./data/vm.txt') as f:
    for line in f.readlines():
        m = re.match('(\S+)\s+(.*)$',line)
        appid = m.group(1)
        vm = m.group(2)
        region = ''
        
        if(re.match('.*VB0[127].*\-(M|LS)$',appid) or
           re.match('.*[ID]AAS.*\-(M|LS)$',appid)):
            region = 'OSAKA'
        elif(re.match('.*VB0[89].*\-(M|LS)$',appid)):
            region = 'TOKYO'
        elif(re.match('.*TKY',appid) or
           re.match('.*TOKYO',appid) or
           re.match('.*VB0[127]',appid) or
           re.match('.*[ID]AAS_MGMT',appid) or
           re.match('.*POD_MGMT',appid) or
           re.match('.*\-VSM$',appid)):
            region = 'TOKYO'
        elif(re.match('.*OSK',appid) or
           re.match('.*OSAKA',appid) or
           re.match('.*VB0[89]',appid)):
            region = 'OSAKA'
        else:
            raise Exception("Region not found for %s" % appid)
        if not region in appids:
            appids[region] = {}
        appids[region][appid] = {'VM':vm}
        
csv = csv.writer(sys.stdout)
for region in ['TOKYO','OSAKA']:
    for appid in sorted(appids[region].keys()):
        csv.writerow([region,appid,appids[region][appid]['VM']])

# print json.dumps(appids,indent=4)