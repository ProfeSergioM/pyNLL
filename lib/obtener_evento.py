#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 22 15:47:56 2021

@author: sergio.morales
"""

def obtener_evento(year,idev):
    import sys
    sys.path.append('/mnt/puntodiez/pyovdas_lib/')
    import pandas as pd
    import ovdas_getfromdb_lib as gdb

    pd.options.mode.chained_assignment = None  # default='warn'
    eventos = gdb.extraer_eventos(str(year)+'-01-01',str(year)+'-12-31',volcan='*',ml='>0')
    eventos = pd.DataFrame(eventos)
    print(eventos)
    evsel = eventos[eventos.idevento==idev]
    print(evsel)
    volcanes =gdb.get_metadata_volcan('*',rep='y')
    volcanes = volcanes.drop_duplicates(subset='nombre', keep="first")
    voldf = volcanes[volcanes.id==evsel.idvolc.iloc[0]]  
    import xarray as xr
    data = xr.load_dataset('/home/sismologia/nc/'+
                           str(voldf.id_zona.values[0])+'/'+
                           str(voldf.cod.values[0])+'.nc')
    dem = data.fillna(0)
    return evsel,voldf,dem