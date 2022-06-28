#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 27 09:43:40 2021

@author: sergio.morales
"""

def create_custom_model(modname):
    mod= 'custom_inputs/'+modname+'.nd'
    from obspy.taup import TauPyModel,taup_create
    import pandas as pd
    #taup_create.build_taup_model(mod)
    #model = TauPyModel(model=modname) 
    rows=[]
    lines = open(mod).read().splitlines()
    lines = open(mod).read().splitlines()
    for i in range(0,len(lines)):
        if len(lines[i].split())==4:
            mod_1D_vP = (lines[i].split()[1])
            mod_1D_vS = (lines[i].split()[2])
            mod_1D_z  = (lines[i].split()[0])
            rows.append([mod_1D_z,mod_1D_vP,mod_1D_vS])
    df_model = pd.DataFrame(rows).rename(columns={0:'prof',1:'vP',2:'vS'}) #df de fases a usar en el sintético
    #return model,df_model.iloc[::2]
    return df_model.iloc[::2]