#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 28 14:35:05 2021

@author: sergio.morales
"""

def create_Time2EQ_input(fasesname,randomint,locname,vPvS):
    outdir_Time2EQ_input= './inputs/5_Time2EQ_input_syn_'+randomint
    lines_loc = open('custom_inputs/'+locname+'.ovd').read().splitlines()
    loc_lon = float(lines_loc[0].split()[0])
    loc_lat = float(lines_loc[0].split()[1])
    loc_pro = -1*float(lines_loc[0].split()[2])
    voldf=[loc_lat,loc_lon,-1*loc_pro]
    tipo='evento'
    from lib.create_common_variables import create_common_variables
    com_CONTROL, com_TRANS = create_common_variables(voldf,randomint,tipo)
    import pandas as pd
    import sys
    import numpy as np
    sys.path.append('/mnt/puntodiez/pyovdas_lib/')
    import ovdas_getfromdb_lib as gdb  
    esta_meta = gdb.get_metadata_wws('*')
    esta_meta = esta_meta[esta_meta.tipo=='SISMOLOGICA']
    esta_meta['tiposism'] = esta_meta.cod.str[0]
    esta_meta = esta_meta[esta_meta.tiposism=='S']
    
    lines = open('custom_inputs/'+fasesname+'.ovd').read().splitlines()
    rows=[]
    for i in range(0,len(lines)):
        sta = (lines[i].split()[0])
        fase = (lines[i].split()[1])
        if sta[0]=='_':
            print('estación sintética')
            stalat=float(lines[i].split()[2])
            stalon=float(lines[i].split()[3])
            staele=float(lines[i].split()[4])
            tipo='syn'
        else:
            stalat = float(esta_meta[esta_meta.codcorto==sta].latitud.iloc[0])
            stalon = float(esta_meta[esta_meta.codcorto==sta].longitud.iloc[0])
            staele = float(esta_meta[esta_meta.codcorto==sta].altitud.iloc[0])
            tipo='ovd'
        if fase=='P':
            faseP=True
            faseS=False
        elif fase=='PS':
            faseP=True
            faseS=True
        rows.append([sta,faseP,faseS,stalat,stalon,staele,tipo])
    df_fases = pd.DataFrame(rows).rename(columns={0:'sta',1:'faseP',2:'faseS',3:'stalat',
                                                  4:'stalon',5:'staele',6:'tipoest'}) #df de fases a usar en el sintético

    
    com_EQFILES = 'EQFILES time/layer ./obs/'+str(randomint)+'_syn.obs'
    com_EQMOD = 'EQMODE SRCE_TO_STA'
    com_EQSRCE = 'EQSRCE '+str(randomint)+' LATLON '+str(loc_lat)+' '+str(loc_lon)+' 0.0 '+str(loc_pro)
    com_EQQUAL2ERR = 'EQQUAL2ERR 0.1 0.2 0.4 0.8 99999.9'
    staline = []
    for index,row in df_fases.iterrows():
        staline.append('EQSTA '+row.sta+'Z P      GAU  0.1    GAU  0.1')
        if row.faseS==True:
            staline.append('EQSTA '+row.sta+'Z S      GAU  0.2    GAU  0.2')
    com_EQSTA = staline
    com_EQVPVS = 'EQVPVS '+vPvS
    file = open(outdir_Time2EQ_input, "w") 
    with open(outdir_Time2EQ_input, 'a') as the_file:
        the_file.write(com_CONTROL+'\n'+com_TRANS+'\n'+com_EQFILES+'\n'+com_EQMOD+'\n'+com_EQSRCE+'\n'+com_EQVPVS+'\n'+com_EQQUAL2ERR)
        for line in com_EQSTA:
            the_file.write('\n'+line)
        file.close()   
    return df_fases,voldf,outdir_Time2EQ_input