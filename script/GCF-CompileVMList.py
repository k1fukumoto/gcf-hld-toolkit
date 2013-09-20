#!/usr/bin/python

import json
import re

appids = {}
with open('./data/vm.txt') as f:
    for line in f.readlines():
        m = re.match('(\S+)\s+(.*)$',line)
        appids[ m.group(1) ] = {'VM':m.group(2)}
        
print json.dumps(appids,indent=4)