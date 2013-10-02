#!/usr/bin/python

import xml.etree.ElementTree as et
import sys, re, csv
from pysphere import VIServer,MORTypes
from util import logger,ErrorCode
from pprint import pprint as pp


known_errors = et.parse('./data/GCF-KnownErrors.xml').getroot()
def ERROR(code,appcode,s):
    l = "%s %s %s" % (code,appcode,s)
    for ke in known_errors.iter('Error'):
        if(ke.attrib['ErrorCode'] == code and
           ke.attrib['AppCode'] == appcode):
            logger.warning(l)
            logger.warning("  >> %s",ke.attrib['Description'])
            return
    logger.error(l)

clstrid_d = {}
clstrname_d = {}
for row in csv.reader(open('./data/GCF-Cluster.csv')):
    clstrid_d[row[0]] = row[1]
    clstrname_d[row[1]] = row[0]

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
    
        logger.debug("Trying to connect %s" % vcip)
        vc.connect(vcip,'sbgcf\\svc_report','VMwar3!!')
        cur_region = region

        try:
            host_d = {}
            vm_d = {}
            for c_mor, c_name in vc.get_clusters().items():
                if(not c_name in clstrname_d): continue
                logger.debug("Fetching cluster '%s'",c_name)
                for h_mor,h_name in vc.get_hosts(from_mor=c_mor).items():
                    logger.debug("Fetching host %s",h_name)
                    host_d[h_name] = c_name
                    for v_mor, v_name in vc._get_managed_objects(MORTypes.VirtualMachine, from_mor=h_mor).items():
                        vm_d[v_name] = h_name
        except:
            raise Exception("Failed to query VM list from vCenter %s" % vcip)

    is_replica = re.match('.+REPLICA',appid)

    if(not vm in vm_d):
        if(is_replica):
            ERROR(ErrorCode.E_MISSING_REPLICA,appid," (%s)" % vm)
        else:
            ERROR(ErrorCode.E_MISSING_VM,appid," (%s)" % vm)
        continue      
    
    m = re.match('(\S+-\S+-\S+-\S+-(AMP|MGMT))',appid)
    clstrid = m.group(1)

    if(clstrid_d[clstrid] != host_d[vm_d[vm]]):
        ERROR(ErrorCode.E_WRONG_CLUSTER,appid,"| Actual %s" % clstrname_d[host_d[vm_d[vm]]])
    
    vmo = None
    try:
        vmo = vc.get_vm_by_name(vm)
        osstr = vmo.get_property('guest_full_name')
    except:
        raise Exception("Failed to get VM object %s (%s)",appid,vm)

    if(is_replica and (not re.match('.+-(M|LS)$',appid))):
        if(vmo.is_powered_off()):
            logger.info ("VERIFIED %s (%s/%s)",appid,vm,osstr)
        else:
            logger.error ("Replica VM is running %s (%s)",appid,vm)
    else:
        if(vmo.is_powered_on()):
            logger.info ("VERIFIED %s (%s/%s)",appid,vm,osstr)
        else:
            logger.error ("VM not running %s (%s)",appid,vm)
        
