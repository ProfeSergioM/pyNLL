#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 22 16:06:40 2021

@author: sergio.morales
"""

def create_Vel2Grid_input(voldf,randomint,yNum,zNum,gridsize,VpVs,ro,tipo,df_model,nref,maxZ): 
    from lib.create_common_variables import create_common_variables
    from lib.get_layers import get_layers
    
    
    com_CONTROL, com_TRANS = create_common_variables(voldf,randomint,tipo)
    com_VGOUT   = "VGOUT ./model/layer"
    com_VGTYPE  = "VGTYPE P"
    if tipo=='volcan':
        maxZ = float(voldf.altitud.iloc[0]/1000)*-1
        outdir_VEL2Grid_input= './inputs/1_Vel2Grid_input_'+voldf.nombre_db.iloc[0]
    elif tipo=='evento':
        maxZ = maxZ*-1
        outdir_VEL2Grid_input= './inputs/1_Vel2Grid_input_syn_'+randomint
    com_VGGRID  = ("VGGRID 2 "+str(yNum)+' '+str(zNum)+' 0.0 0.0 '+str(maxZ)+' ' 
               +str(gridsize)+' '+str(gridsize)+' '+str(gridsize)+' SLOW_LEN')
    if tipo=='volcan':
        com_LAYERS,lasttop = get_layers(voldf,VpVs,ro)
    elif tipo=='evento':
        layers = []
        for index, row in df_model.iterrows():
            prof=str(float(row.prof)-nref/1000)
            vP=str(row.vP)
            vS=str(row.vS)
            ro=str(ro)
            linea='LAYER '+prof+' '+vP+ ' 0.00 '+vS+' 0.0 '+ro+ ' 0.0'
            layers.append(linea)
        com_LAYERS=layers
        lasttop=None
    file = open(outdir_VEL2Grid_input, "w") 
    with open(outdir_VEL2Grid_input, 'a') as the_file:
        the_file.write(com_CONTROL+'\n'+com_TRANS+'\n'+com_VGOUT+'\n'+com_VGTYPE+'\n'+com_VGGRID)
        for line in com_LAYERS:
            the_file.write('\n'+line)
        file.close()
    return outdir_VEL2Grid_input,lasttop