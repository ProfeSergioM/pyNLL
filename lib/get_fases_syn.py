#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 27 10:02:50 2021

@author: sergio.morales
"""

def get_fases_syn(model,confname,df_model,fasesname,locname):
    from lib.get_delay import get_delay
    from obspy.taup.taup_geo import calc_dist
    import pandas as pd
    import sys
    import numpy as np
    sys.path.append('//172.16.40.10/sismologia/pyovdas_lib/')
    import ovdas_getfromdb_lib as gdb  
    esta_meta = gdb.get_metadata_wws('*')
    esta_meta = esta_meta[esta_meta.tipo=='SISMOLOGICA']
    esta_meta['tiposism'] = esta_meta.cod.str[0]
    esta_meta = esta_meta[esta_meta.tiposism=='S']
    
    lines_ref = open('custom_inputs/'+confname+'.ovd').read().splitlines()
    for i in range(0,len(lines_ref)):
        if (lines_ref[i].split()[0])=='nref':
            nref=lines_ref[i].split()[1]
        elif (lines_ref[i].split()[0])=='vPvS':
            vPvS=float(lines_ref[i].split()[1])
    
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
    ###
    lines_loc = open('custom_inputs/'+locname+'.ovd').read().splitlines()
    loc_lon = float(lines_loc[0].split()[0])
    loc_lat = float(lines_loc[0].split()[1])
    
    loc_pro = float(lines_loc[0].split()[2])+int(nref)/1000 #coordenadas del evento sintético
    loc_pro_abs = float(lines_loc[0].split()[2])
    tps,tss=[],[]
    for index,row in df_fases.iterrows():
        #distalat = row.stalat - loc_lat
        #distalon = row.stalon - loc_lon
        #ev_dista_deg = np.sqrt(distalat**2+distalon**2)
        ev_dista_deg = calc_dist(loc_lat,loc_lon,float(row.stalat),float(row.stalon),6378.137,1/298.257223563)
        tp = model.get_travel_times(source_depth_in_km=loc_pro,
                                    distance_in_degree=ev_dista_deg,
                                    phase_list=['P','p'],
                                    receiver_depth_in_km=0)
        ts = model.get_travel_times(source_depth_in_km=loc_pro,
                                    distance_in_degree=ev_dista_deg,
                                    phase_list=['S','s'],
                                    receiver_depth_in_km=0)
        tiempo_p = float(str(tp[0]).split()[-2])
        delayP = get_delay(df_model,nref,row.staele)
        tiempo_p= tiempo_p+ delayP
        tps.append(tiempo_p)
        if row.faseS==True:
            delayS = vPvS*delayP
            tiempo_s = float(str(ts[0]).split()[-2])
            tiempo_s = tiempo_s+delayS
            tss.append(tiempo_s)
        else:
            tss.append(np.nan)
        
    df_fases['tP']=tps
    df_fases['tS']=tss
    return df_fases,[loc_lat,loc_lon,loc_pro_abs]