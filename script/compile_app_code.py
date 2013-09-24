#!/usr/bin/env python

import xml.etree.ElementTree as et
import csv,re

pods = et.parse('./data/GCF-Pod.xml').getroot()
modules = et.parse('./data/GCF-Module.xml').getroot()
appids = csv.reader(open('./data/GCF-VM.csv'))

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
        print 
        m = re.match("\S+-\S+-\S+-\S+-(\S+)_MGMT_REPLICA_(VB\d{2})-(\S+)",code) 
        if(not m): raise Exception("ERROR appcode %s not found"  % code)
        
        rep = m.group(1)
        vb = m.group(2)
        ac = m.group(3)
        pat = "%s-%s_MGMT-%s" %(vb,rep,ac)
        for ac in appid_d.keys():
            if(re.match('.*' + pat,ac)):
                print ("%s,%s" % (code,appid_d[ac]))
                return
        raise Exception("ERROR primary appcode for %s not found" % code)
    
for pod in pods:
    if('Skip' in pod.attrib): continue
    for region in pod:
        for dc in region:
            for vb in dc:
                for mod in vb.findall('Module'):
                    opt_app = False
                    if('Option' in mod.attrib): opt_app = mod.attrib['Option']
                    for app in mod_d[code(mod)]:
                        if('Optional' in app.attrib):
                            if(code(app) != opt_app): 
                                continue
                        for node in app:
                            nodestr = code(node)
                            if (len(nodestr) > 0):
                                nodestr = "-" + nodestr
                            modstr = code(mod)
                            if('Primary' in mod.attrib):
                                modstr = "%s_%s" % (modstr,mod.attrib['Primary'])
                            codestr = ("%s-%s-%s-%s-%s-%s%s" % (code(pod),code(region),code(dc),code(vb),modstr,code(app),nodestr))
                            if ('Count' in mod.attrib):
                                for i in range(int(mod.attrib['Count'])):
                                    on_appcode ("%s-%02d" % (codestr,i+1))
                            else:
                                on_appcode (codestr)
             
    