#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 22 17:17:24 2021

@author: sergio.morales
"""

def create_NLLoc_input(randomint,voldf,signature,evsel,stacod,vPvS,tipo,maxZ):
    from lib.create_common_variables import create_common_variables
    com_CONTROL, com_TRANS = create_common_variables(voldf,randomint,tipo)  
    com_LOCMETH     = 'LOCMETH EDT_OT_WT 9999.0 4 -1 -1 1.68 6 -1.0 1'
    com_LOCGAU      = 'LOCGAU 0.2 0.0'
    com_LOCGAU2     = 'LOCGAU2 0.01 0.05 2.0'
    com_PHASEID1    = 'LOCPHASEID  P   P p G PN PG'
    com_PHASEID2    = 'LOCPHASEID  S   S s G SN SG'
    com_LOCQUAL2ERR = 'LOCQUAL2ERR 0.1 0.5 1.0 2.0 3.0 4.0 5.0 6.0 7.0 99999.9'
    com_LOCANGLES   = 'LOCANGLES ANGLES_YES 5'
    com_LOCMAG      = 'LOCMAG ML_HB 1.0 1.110 0.00189'
    com_LOCPHSTAT   = 'LOCPHSTAT 9999.0 -1 9999.0 1.0 1.0 9999.9 -9999.9 9999.9'
    com_LOCHYPOUT   = 'LOCHYPOUT SAVE_NLLOC_ALL  SAVE_HYPOINV_SUM'
    com_LOCSEARCH   = 'LOCSEARCH  OCT 10 10 10 0.001 50000 5000 0 1'
    com_LOCSIG      = 'LOCSIG '+str(signature)
    if tipo=='volcan':
        outdir_NLLoc_input = './inputs/4_NLLoc_input_'+voldf.nombre_db.iloc[0]
        com_LOCCOM      = 'LOCCOM Localizacion de evento id:'+str(evsel.idevento.iloc[0])
        com_LOCFILES    = 'LOCFILES ./obs/'+str(evsel.idevento.iloc[0])+'.obs NLLOC_OBS ./time/layer  ./loc/'+str(evsel.idevento.iloc[0])
        volpeak = float(voldf.altitud.iloc[0]/1000)*-1
        com_LOCGRID     = 'LOCGRID  101 101 101  -50.0 -50.0 '+str(volpeak)+'  1 1 1   PROB_DENSITY  SAVE'
    elif tipo=='evento':
        outdir_NLLoc_input = './inputs/4_NLLoc_input_syn_'+randomint
        com_LOCCOM      = 'LOCCOM Localizacion de evento sintetico, randomint:'+randomint
        com_LOCFILES    = 'LOCFILES ./obs/'+randomint+'_syn.obs NLLOC_OBS ./time/layer  ./loc/'+randomint
        com_LOCGRID     = 'LOCGRID  101 101 101  -50.0 -50.0 '+str(-maxZ)+'  1 1 1   PROB_DENSITY  SAVE'
    file = open(outdir_NLLoc_input, "w") 
    with open(outdir_NLLoc_input, 'a') as the_file:
        the_file.write(com_CONTROL+'\n'+com_TRANS+'\n'+com_LOCSIG+'\n'+com_LOCCOM+'\n'+com_LOCFILES+'\n'+com_LOCHYPOUT+'\n'+com_LOCSEARCH+'\n'+com_LOCGRID+'\n'+
                       com_LOCMETH+'\n'+com_LOCGAU+'\n'+com_LOCGAU2+'\n'+com_PHASEID1+'\n'+com_PHASEID2+'\n'+com_LOCQUAL2ERR+'\n'+com_LOCANGLES+'\n'+
                       com_LOCMAG+'\n'+com_LOCPHSTAT)
        file.close()  
    return outdir_NLLoc_input