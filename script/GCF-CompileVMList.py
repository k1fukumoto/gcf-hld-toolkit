#!/usr/bin/python

from pprint import pprint
import json

appid = {}
with open('./data/vm.txt') as f:
    for line in f.readlines():
        appid_vm = line.split()
        appid[ appid_vm[0] ] = {'VM':appid_vm[1]}
        
print json.dumps(appid,indent=4)