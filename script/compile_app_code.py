#!/usr/bin/env python

import xml.etree.ElementTree as et
import csv

pods = et.parse('./data/GCF-Pod.xml').getroot()
modules = et.parse('./data/GCF-Module.xml').getroot()
appids = csv.reader(open('./data/GCF-AppCode.csv'))

appid_d = {}
for row in appids:
    appid_d[row[0]] = row[1]

mod_d = {}
for mod in modules:
    mod_d[mod.attrib['Code']] = mod 


def get_applications(mod):
    modcode = code(mod)

    if(not modcode in mod_d):
        raise Exception("Unresolved module code '%s'" % modcode)
    
    is_replica = ('Replica' in mod.attrib)

    # Build dictionary for optional applications
    include_apps = {}
    exclude_apps = {}
    for opt in mod.findall('Option'):
        if('Exclude' in opt.attrib):
            exclude_apps[code(opt)] = True
        else:
            include_apps[code(opt)] = True

    ret = []
    for app in mod_d[modcode]:
        if(is_replica and
           not 'Replicated' in app.attrib): 
            continue
        if(code(app) in exclude_apps):
            continue
        if( 'Optional' in app.attrib and
            not (code(app) in include_apps) ):
            continue
        ret.append(app)

    return ret

def code(e):
    return e.attrib['Code']

def on_appcode(code):
    if(code in appid_d):
        print ("%s,%s" % (code,appid_d[code]))
    else:
        raise Exception("ERROR appcode %s not found"  % code)
    
def on_application(pod,region,dc,vb,clstr,mod,app):
    is_replica = ('Replica' in mod.attrib)

    # Add suffix for replica modeuls
    modcode = code(mod)
    if(is_replica):
        modcode = "%s_REPLICA_%s" % (modcode,mod.attrib['Replica'])
        
    # Add suffix when Vblock attribute is given. i.e., VSM
    if('Vblock' in mod.attrib):
        modcode = "%s_%s" % (modcode,mod.attrib['Vblock'])
        
     # Change cluster, if explicity specifiec
    clstrcode = code(clstr)
    if('Cluster' in app.attrib):
        clstrcode = app.attrib['Cluster']   
        
    codestr = ("%s-%s-%s-%s-%s-%s-%s" % (code(pod),code(region),code(dc),code(vb),clstrcode,modcode,code(app)))

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
    if('Exclude' in pod.attrib): continue
    for region in pod:
        for dc in region:
            for vb in dc:
                for clstr in vb:
                    for mod in clstr:
                        for app in get_applications(mod):
                            on_application(pod,region,dc,vb,clstr,mod,app)

                                