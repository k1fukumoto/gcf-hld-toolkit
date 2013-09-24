#!/usr/bin/python

import os, sys, re, csv
from pysphere import VIServer

def log(l):
    print(l)
    with open('./log/verify_vm_inventory.log','a') as f: f.write(l+"\n")
    
def INFO(s):
    log("INFO: %s" % s)

def ERROR(s):
    log("ERROR: %s" % s)

try: os.remove('./log/verify_vm_inventory.log')
except: ''

# csv = csv.reader(open('./data/GCF-VM.csv'))
csv = csv.reader(sys.stdin)

vc = VIServer()
cur_region = None
for row in csv:
    appid = row[0]
    vm = row[1]

    region = ''
    m = re.match('.*(TOKYO|OSAKA)',appid)
    if(m): region = m.group(1)

    if(cur_region != region):
        vcip = None
        if(region == 'TOKYO'):
            vcip = '10.1.1.50'
        else:
            vcip = '10.1.8.50'
    
        print("INFO: Trying to connect %s" % vcip)
        vc.connect(vcip,'sbgcf\\svc_report','VMwar3!!')
        cur_region = region

    vmo = None
    try:
        vmo = vc.get_vm_by_name(vm)
    except:
        ERROR ("VM not found %-16s (%s)" % (appid,vm))
        continue

    
    try:
        if(re.match('.*REPLICA',appid)):
            if(vmo.is_powered_off()):
                INFO ("Verified %-16s (%s)" % (appid,vm))
            else:
                ERROR ("Replica VM is running %-16s (%s)" % (appid,vm))
        else:
            if(vmo.is_powered_on()):
                INFO ("Verified %-16s (%s)" % (appid,vm))
            else:
                ERROR ("VM not running %-16s (%s)" % (appid,vm))
    except:
        ERROR("VM query error %-16s (%s)" % (appid,vm))
        continue
        
