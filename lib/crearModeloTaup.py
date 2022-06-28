#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 28 09:48:55 2021

@author: sergio.morales
"""

def crearModeloTaup(volcan,vPvS,nombremod):
    import sys
    sys.path.append('/mnt/puntodiez/pyOvdas_lib')
    import ovdas_getfromdb_lib as gdb        
    volcanes =gdb.get_metadata_volcan(volcan,rep='y')
    voldf = volcanes.drop_duplicates(subset='nombre', keep="first")
    print(voldf.nref)
    import numpy as np
    lines = open('/mnt/puntodiez/pyOvdas_lib/mod/'+str(voldf.id.iloc[0])+'.txt').read().splitlines()[:-2]
    profs,velPs,velSs=[],[],[]
    for i in range(0,len(lines)):
        prof = float(lines[i].split()[1])
        vP = float(lines[i].split()[0])
        #prof = str(np.round(prof-voldf.nref.iloc[0]/1000,2))
        
        profs.append(prof)
        if i>0:
            profs.append(prof)
        if i<len(lines)-1:
            velPs.append(vP)
            velPs.append(vP)
            velSs.append(str(np.round(vP/vPvS,2)))
            velSs.append(str(np.round(vP/vPvS,2)))
        else:
            velPs.append(vP)
            velSs.append(vP/vPvS)
    lines=[]
    for j in range(0,len(profs)):
        lines.append([profs[j],velPs[j],velSs[j],'999'])
    lines.append(['mantle','',''])
    lines.append(['2891.0','13.71',str(np.round(np.float('13.71'),2)/vPvS),'999'])
    lines.append(['outer-core','',''])
    lines.append(['2891.0','8.06',str(np.round(np.float('8.06'),2)/vPvS),'999'])
    lines.append(['5149.5','10.35',str(np.round(np.float('10.35'),2)/vPvS),'999'])
    lines.append(['inner-core','',''])
    lines.append(['5149.5','11.02',str(np.round(np.float('11.02'),2)/vPvS),'999'])
    import csv   
    with open('custom_inputs/'+nombremod+'.nd', "w", newline="") as f:
        writer = csv.writer(f,delimiter='\t')
        writer.writerows(lines)
    from obspy.taup import TauPyModel,taup_create
    taup_create.build_taup_model('custom_inputs/'+nombremod+'.nd')
    model = TauPyModel(model=nombremod)
    return model