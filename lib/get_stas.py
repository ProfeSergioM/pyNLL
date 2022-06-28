#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 22 17:09:47 2021

@author: sergio.morales
"""

def get_stas(evsel):
    import sys
    sys.path.append('//172.16.40.10/sismologia/pyovdas_lib/')
    import ovdas_getfromdb_lib as gdb
    estadf = gdb.get_metadata_wws(volcan='*',estadoInst='*',estadoEst='*')
    fases = gdb.get_fasesLoc(evsel.idevento.iloc[0], evsel.fecha.iloc[0].year)
    staline = []
    stacods =[]
    for index,row in fases.iterrows():
        try:
            stacod = str(row.cod)
            stacods.append(stacod)
            stalat = str(estadf[estadf.codcorto==stacod[1:]].latitud.iloc[0])
            stalon = str(estadf[estadf.codcorto==stacod[1:]].longitud.iloc[0])
            stahei = str(estadf[estadf.codcorto==stacod[1:]].altitud.iloc[0]/1000)
            staline.append('GTSRCE '+stacod[1:]+'Z LATLON '+stalat+' '+stalon+' 0.0 '+stahei)
        except:
            print('Estación '+stacod+' no ingresada a db')
    return staline,stacods