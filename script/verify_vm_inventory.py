#!/usr/bin/python

import sys, re, csv
from pysphere import VIServer
from util import logger

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
    
        logger.info("Trying to connect %s" % vcip)
        vc.connect(vcip,'sbgcf\\svc_report','VMwar3!!')
        cur_region = region

    vmo = None
    try:
        vmo = vc.get_vm_by_name(vm)
    except:
        logger.error("VM not found %s (%s)",appid,vm)
        continue

    
    if(re.match('.+REPLICA',appid) and (not re.match('.+-(M|LS)$',appid))):
        if(vmo.is_powered_off()):
            logger.info ("Verified %s (%s)",appid,vm)
        else:
            logger.error ("Replica VM is running %s (%s)",appid,vm)
    else:
        if(vmo.is_powered_on()):
            logger.info ("Verified %s (%s)",appid,vm)
        else:
            logger.error ("VM not running %s (%s)",appid,vm)
        
