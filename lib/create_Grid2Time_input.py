#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 22 16:06:40 2021

@author: sergio.morales
"""

def create_Grid2Time_input(evsel,voldf,randomint,tipo,df_sta): 
    from lib.create_common_variables import create_common_variables
    from lib.get_stas import get_stas
    com_GTFILES = 'GTFILES  ./model/layer  ./time/layer P'
    com_GTMODE =  'GTMODE GRID2D ANGLES_YES'
    com_GT_PLFD = 'GT_PLFD  1.0e-3  0'
    com_CONTROL, com_TRANS = create_common_variables(voldf,randomint,tipo)
    if tipo=='volcan':
        outdir_Grid2Time_input= './inputs/2_Grid2Time_input_'+voldf.nombre_db.iloc[0]
           
        com_GTSRCE,stacods = get_stas(evsel)

    elif tipo=='evento':
        import sys
        sys.path.append('//172.16.40.10/sismologia/pyovdas_lib/')
        import ovdas_getfromdb_lib as gdb
        outdir_Grid2Time_input= './inputs/2_Grid2Time_input_syn_'+randomint
        #estadf = gdb.get_metadata_wws(volcan='*',estadoInst='*',estadoEst='*')
        staline = []
        stacods =[]
        for index,row in df_sta.iterrows():
            stacod = str(row.sta)
            stacods.append(stacod)
            stalat = str(row.stalat)
            stalon = str(row.stalon)
            stahei = str(row.staele/1000)
            #stahei = str(nref/1000)
            staline.append('GTSRCE '+stacod+'Z LATLON '+stalat+' '+stalon+' 0.0 '+stahei)
        com_GTSRCE = staline
        
    file = open(outdir_Grid2Time_input, "w") 
    with open(outdir_Grid2Time_input, 'a') as the_file:
        the_file.write(com_CONTROL+'\n'+com_TRANS+'\n'+com_GTFILES+'\n'+com_GTMODE)
        for line in com_GTSRCE:
            the_file.write('\n'+line)
        the_file.write('\n'+com_GT_PLFD)
        file.close()           
    return outdir_Grid2Time_input,stacods