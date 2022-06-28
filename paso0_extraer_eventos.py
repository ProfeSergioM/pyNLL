#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 15:00:09 2022

@author: sergio
"""

def get_data_evs(ini,fin,volcan,filename):
    import sys
    sys.path.append('/mnt/puntodiez/pyovdas_lib/')
    import pandas as pd
    import ovdas_getfromdb_lib as gdb
    pd.options.mode.chained_assignment = None  # default='warn'

    aer = gdb.extraer_eventos(ini,fin,volcan=volcan)

    aer = pd.DataFrame(aer)
    aer = aer[aer.ml>0]
    aer = aer[aer.nestaciones>8]
    aer = aer[aer.gap<180]
    if len(aer)>10:
    	print('Más de 10 eventos, mostrando los primeros 10 en orden cronologico\n')
    	print(aer.head(10)[['fecha','idevento','ml','tipoevento']])
    else:
    	print(aer)	
    aer.index.name='id'
    aer.to_excel('/mnt/puntocientodos/tmp/pyNLL/'+filename+'.xlsx')
    
   
import sys
get_data_evs(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])
