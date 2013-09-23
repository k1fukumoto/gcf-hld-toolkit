#!/usr/bin/python

import csv
import xml.etree.ElementTree as et

et.parse('./data/GCF-Servicde.xml')

from pysphere import VIServer

csv = csv.reader(open('./data/GCF-VM.csv'))

vc = VIServer()
cur_region = None
for row in csv:
    region = row[0]
    appid = row[1]
    vm = row[2]

    if(cur_region != region):
        vcip = None
        if(region == 'TOKYO'):
            vcip = '10.1.1.50'
        else:
            continue
            vcip = '10.1.8.50'
    
        print("INFO: Trying to connect %s" % vcip)
        vc.connect(vcip,'sbgcf\\svc_report','VMwar3!!')
        cur_region = region

    vmo = None
    try:
        vmo = vc.get_vm_by_name(vm)
    except:
        print ("ERROR: VM not found %-16s (%s)" % (appid,vm))
        continue

    if('POWERED ON' == vmo.get_status()):
        print ("INFO: Verified %-16s (%s)" % (appid,vm))
    else:
        print ("ERROR: VM not running %-16s (%s)" % (appid,vm))
