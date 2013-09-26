#!/usr/bin/python

import sys, re, csv
from pysphere import VIServer,MORTypes
from util import logger

# csv = csv.reader(open('./data/GCF-VM.csv'))
csv = csv.reader(sys.stdin)

vc = VIServer()
cur_region = None
host_d = {}
vm_d = {}
for row in csv:
    appid = row[0]
    vm = row[1]

    region = ''
    m = re.match('.*(TOKYO|OSAKA)',appid)
    if(m): 
        region = m.group(1)
    else:
        logger.critical("Invalid appid with no region name %s",appid)

    if(cur_region != region):
        vcip = None
        if(region == 'TOKYO'):
            vcip = '10.1.1.50'
        else:
            vcip = '10.1.8.50'
    
        logger.info("Trying to connect %s" % vcip)
        vc.connect(vcip,'sbgcf\\svc_report','VMwar3!!')
        cur_region = region

#        for c_mor, c_name in vc.get_clusters().items():
#            for h_mor,h_name in vc.get_hosts(from_mor=c_mor).items():
#                host_d[h_name] = c_name
#                for v_mor, v_name in vc._get_managed_objects(MORTypes.VirtualMachine, from_mor=h_mor).items():
#                    print ("%s, %s, %s" % (c_name,h_name,v_name))

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
        
