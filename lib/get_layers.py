#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 22 16:08:26 2021

@author: sergio.morales
"""
def get_layers(voldf,VpVs,ro):
    import numpy as np
    lines = open('/mnt/puntodiez/pyovdas_lib/mod/'+str(voldf.id.iloc[0])+'.txt').read().splitlines()[:-2]
    layers = []
    for line in lines:
        line = line.split(' ')
        prof = float(line[-1])-voldf.nref.iloc[0]/1000
        linea='LAYER '+str(prof)+' '+line[2]+ ' 0.00 '+str(np.round(float(line[2])/VpVs,2))+' 0.0 '+str(ro)+ ' 0.0'
        layers.append(linea)
    return layers,line[-1]