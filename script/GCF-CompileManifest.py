import json
import re

services = json.load(open('./GCF-Manifest-Service.json'))

pods = json.load(open('./GCF-Manifest-POD.json'))

for pod, v in pods.items():
    for geo, v in v.items():
        for dc, v in v.items():
            for vb, v in v.items():
                for s in v["Services"]:
                    for app, nodes in services[s]['Applications'].items():
                        for node in nodes:
                            if(node != ''): 
                                node = "-%s" % node
                            if(re.match('^POD', s)):
                                print("%s-%s-%s%s" % (s, pod, app,node))
                            elif(re.match('^GEO', s)):
                                print("%s-%s-%s%s" % (s, geo, app,node))
                            elif(re.match('^DC', s)):
                                print("%s-%s-%s%s" % (s, dc, app,node))
                            elif(re.match('^VB', s) or re.match('^ESX', s)):
                                print("%s-%s-%s%s" % (s, vb, app,node))
                            else:
                                print("%s-%s%s" % (s, app,node))


    

