#!/usr/bin/env python

import xml.etree.ElementTree as et
import csv

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
    print ("%s,%s" % (code,appid_d[code]))
    
for pod in pods:
    if('Skip' in pod.attrib): continue
    for region in pod:
        for dc in region:
            for vb in dc:
                for mod in vb.findall('Module'):
                    for app in mod_d[code(mod)]:
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
             
    