#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 27 10:00:04 2021

@author: sergio.morales
"""

def create_custom_conf(confname):
    lines_ref = open('custom_inputs/'+confname+'.ovd').read().splitlines()
    for i in range(0,len(lines_ref)):
        if (lines_ref[i].split()[0])=='yNum':
            yNum=int(lines_ref[i].split()[1])
        elif (lines_ref[i].split()[0])=='zNum':
            zNum=int(lines_ref[i].split()[1])
        elif (lines_ref[i].split()[0])=='gsize':
            gridsize=float(lines_ref[i].split()[1])
        elif (lines_ref[i].split()[0])=='nref':
            nref=float(lines_ref[i].split()[1])
            maxZ=nref/1000
        elif (lines_ref[i].split()[0])=='ro':
            ro=float(lines_ref[i].split()[1])
        elif (lines_ref[i].split()[0])=='sign':
            signature=lines_ref[i].split()[1]
        elif (lines_ref[i].split()[0])=='vPvS':
            vPvS=lines_ref[i].split()[1]   
        elif (lines_ref[i].split()[0])=='zmax':
            zmax=lines_ref[i].split()[1]   
    return yNum,zNum,gridsize,nref,maxZ,ro,signature,vPvS,zmax