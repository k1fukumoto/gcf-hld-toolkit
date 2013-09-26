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
    
def on_module(pod,region,dc,vb,clstr,mod):
    # If "Primary" is specified, append it to module
    modstr = code(mod)
    if('Primary' in mod.attrib):
        modstr = "%s_%s" % (modstr,mod.attrib['Primary'])

    # Build dictionary for optional applications
    opt_app = {}
    for opt in mod.findall('Option'):
        opt_app[code(opt)] = True
    
    # Iterate through all applications in module
    for app in mod_d[code(mod)]:
        # If application is marked as optional, skip unless it is in optional-apps dictionary
        if('Optional' in app.attrib):
            if(not code(app) in opt_app): 
                continue

        # Iterate through each node in application
        for node in app:
            nodestr = code(node)
            # Add node suffix, only when it is not empty
            if (len(nodestr) > 0):
                nodestr = "-" + nodestr

            codestr = ("%s-%s-%s-%s-%s-%s-%s%s" % (code(pod),code(region),code(dc),code(vb),code(clstr),modstr,code(app),nodestr))
    
            # If "Count" is specified in module, iterate through it with numeric suffix
            if ('Count' in mod.attrib):
                for i in range(int(mod.attrib['Count'])):
                    on_appcode ("%s-%02d" % (codestr,i+1))
            else:
                on_appcode (codestr)
    
for pod in pods:
    if('Skip' in pod.attrib): continue
    for region in pod:
        for dc in region:
            for vb in dc:
                for clstr in vb:
                    for mod in clstr:
                        on_module(pod,region,dc,vb,clstr,mod)
                                