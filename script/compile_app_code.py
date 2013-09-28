#!/usr/bin/env python

import xml.etree.ElementTree as et
import csv,re
from util import logger

pods = et.parse('./data/GCF-Pod.xml').getroot()
modules = et.parse('./data/GCF-Module.xml').getroot()
appids = csv.reader(open('./data/GCF-AppCode.csv'))

appid_d = {}
for row in appids:
    appid_d[row[0]] = row[1]

mod_d = {}
for mod in modules:
    mod_d[mod.attrib['Code']] = mod 

def get_replica_apps(m):
    modcode = code(m)
    apps = []
    
    # Build dictionary for skipped applications
    skip_apps = {}
    for opt in mod.findall('Option'):
        if('Skip' in opt.attrib):
            skip_apps[code(opt)] = True

    if(re.match('.*_REPLICA$',modcode)):
        modcode = modcode.replace('_REPLICA','')
        if(modcode in mod_d):
            for app in mod_d[modcode]:
                if('Replicated' in app.attrib and (not code(app) in skip_apps)): 
                    apps.append(app)
            return apps
        else:
            raise Exception("Unresolved module '%s'" % modcode)
    raise Exception("Unresolved module '%s'" % modcode)


def get_applications(m):
    modcode = code(m)
    apps = mod_d[modcode] if (modcode in mod_d) else get_replica_apps(m)

    # Build dictionary for optional applications
    opt_apps = {}
    for opt in mod.findall('Option'):
        opt_apps[code(opt)] = True

    ret = []
    for app in apps:    
        if( (not 'Optional' in app.attrib) or
            (code(app) in opt_apps) ):
            ret.append(app)
    return ret

def code(e):
    return e.attrib['Code']

def on_appcode(code):
    if(code in appid_d):
        print ("%s,%s" % (code,appid_d[code]))
    else:
        m = re.match("\S+-\S+-\S+-\S+-(\S+)_MGMT_REPLICA_(VB\d{2})-(\S+)$",code) 
        if(not m): raise Exception("ERROR appcode %s not found"  % code)
        
        rep = m.group(1)
        vb = m.group(2)
        ac = m.group(3)
        pat = "%s-%s_MGMT-%s$" %(vb,rep,ac)
        for ac in appid_d.keys():
            if(re.match('.*' + pat,ac)):
                print ("%s,%s" % (code,appid_d[ac]))
                return
        logger.error("Primary appcode for %s not found" % code)
    
def on_application(pod,region,dc,vb,clstr,mod,app):
    # If "Primary" is specified, append it to module
    modcode = code(mod)
    if('Primary' in mod.attrib):
        modcode = "%s_%s" % (modcode,mod.attrib['Primary'])
        
    # Flag whether we're dealing with replica module    
    is_replica = re.match('.*REPLICA',modcode)

    
    codestr = ("%s-%s-%s-%s-%s-%s-%s" % (code(pod),code(region),code(dc),code(vb),code(clstr),modcode,code(app)))

    if ('Count' in mod.attrib):
        for i in range(int(mod.attrib['Count'])):
            on_appcode ("%s-%02d" % (codestr,i+1))
    elif (0 == len(app)):
        on_appcode(codestr)
    else:
        for node in app:
            if (0 == len(code(node))): 
                on_appcode (codestr)
            elif(is_replica):
                if(0 < len(node)):
                    for rep in node:
                        if(0 < len(code(rep))):
                            on_appcode ("%s-%s" % (codestr,code(rep)))
                elif('Replicated' in node.attrib):
                    if(node.attrib['Replicated'] == "true"):
                        on_appcode ("%s-%s" % (codestr,code(node)))
                else: 
                    on_appcode ("%s-%s" % (codestr,code(node)))
            else:
                on_appcode ("%s-%s" % (codestr,code(node)))

for pod in pods:
    if('Skip' in pod.attrib): continue
    for region in pod:
        for dc in region:
            for vb in dc:
                for clstr in vb:
                    for mod in clstr:
                        for app in get_applications(mod):
                            on_application(pod,region,dc,vb,clstr,mod,app)

                                