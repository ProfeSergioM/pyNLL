#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 29 09:14:40 2021

@author: sergio.morales
"""
def do_pyNLL_syn(modname,confname,fasesname,locname):
    import locale
    locale.setlocale(locale.LC_ALL, 'en_US')
    from lib.create_custom_model import create_custom_model
    from lib.prepare_folders import prepare_folders
    from lib.create_custom_conf import create_custom_conf
    from lib.get_fases_syn import get_fases_syn
    from lib.create_Vel2Grid_input import create_Vel2Grid_input
    from lib.create_Grid2Time_input import create_Grid2Time_input
    from lib.create_NLLoc_input import create_NLLoc_input
    from lib.create_Time2EQ_input import create_Time2EQ_input
    from lib.create_obs_input import create_obs_input
    
    from random import randint
    import subprocess
    tipo='evento'
    randomint = str(randint(1,100000))
    lista_carpetas=['inputs','time','model','obs','loc','gmt','custom_inputs']
    limpiar_carpetas=False
    prepare_folders(lista_carpetas, limpiar_carpetas)
    df_model =  create_custom_model(modname)
    yNum,zNum,gridsize,nref,maxZ,ro,signature,vPvS,zmax = create_custom_conf(confname)
    df_sta,evloc,outdir_Time2EQ_input = create_Time2EQ_input(fasesname,randomint,locname,vPvS)
    outdir_Vel2Grid_input,lasttop =create_Vel2Grid_input(evloc,randomint,yNum,zNum,gridsize,vPvS,ro,tipo,df_model,nref,maxZ)
    subprocess.run(['Vel2Grid',outdir_Vel2Grid_input]) #EJECUTA Vel2Grid
    subprocess.run(['Time2EQ',outdir_Time2EQ_input]) #EJECUTA Vel2Grid
    outdir_Grid2Time_input,stacods = create_Grid2Time_input(None, evloc, randomint,tipo,df_sta)
    subprocess.run(['Grid2Time',outdir_Grid2Time_input]) # EJECUTA Grid2Time
    outdir_NLLoc_input = create_NLLoc_input(randomint, evloc, signature, None, stacods,vPvS,tipo,maxZ)
    subprocess.run(['NLLoc',outdir_NLLoc_input]) # EJECUTA NLL
    
    subprocess.run(['LocSum','loc/'+str(randomint)+'.sum.grid0.loc','1','loc/'+str(randomint),'loc/'+str(randomint)+'.*.*.grid0.loc']) # EJECUTA LocSum
    subprocess.run(['Grid2GMT',outdir_Vel2Grid_input,'loc/'+str(randomint),'gmt','L','S']) # EJECUTA LocSum
    import os
    file='gmt'+str(randomint)+'.LS.gmt'
    if os.path.isfile(file):
        os.remove(file)
    from lib.plot_loc_syn import plot_loc_syn
    plot_loc_syn(randomint,evloc,df_sta,nref,zmax)