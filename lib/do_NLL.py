#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 23 09:01:11 2021

@author: sergio.morales
"""

def do_pyNLL(idev,year,limpiar_carpetas,yNum,zNum,gridsize,VpVs,ro,signature):

    tipo='volcan'
    from random import randint
    import os
    randomint = str(randint(1,100000))
    import subprocess
    from lib.obtener_evento import obtener_evento
    from lib.create_Vel2Grid_input import create_Vel2Grid_input
    from lib.create_Grid2Time_input import create_Grid2Time_input
    from lib.create_NLLoc_input import create_NLLoc_input
    from lib.prepare_folders import prepare_folders
    from lib.create_obs_input import create_obs_input
    from lib.plot_results_comparison import plot_results_comparation
    evsel,voldf,dem = obtener_evento(year, idev) #Obtener evento dede la DB
    lista_carpetas = ['inputs','time','model','obs','loc','gmt']
    prepare_folders(lista_carpetas,limpiar_carpetas)
    outdir_Vel2Grid_input,lasttop =create_Vel2Grid_input(voldf,randomint,yNum,zNum,gridsize,VpVs,ro,tipo,None,None,None)
    print(outdir_Vel2Grid_input)
    subprocess.run(['Vel2Grid',outdir_Vel2Grid_input]) #EJECUTA Vel2Grid
    outdir_Grid2Time_input,stacods = create_Grid2Time_input(evsel, voldf, randomint,tipo,None)
    subprocess.run(['Grid2Time',outdir_Grid2Time_input]) #EJECUTA Vel2Grid
    create_obs_input(evsel,tipo,None,None)
    outdir_NLLoc_input = create_NLLoc_input(randomint, voldf, signature, evsel, stacods, VpVs,tipo,None)
    subprocess.run(['NLLoc',outdir_NLLoc_input]) # EJECUTA NLL
    idev = evsel.idevento.iloc[0]
    evento=evsel
    file =(str(evento.idevento.iloc[0])+'.sum.grid0.loc.hyp')
    with open("./loc/"+file) as file_in:
        lines = []
        for line in file_in:
            lines.append(line)
        latNLL = float((lines[6].split(' ')[12])) 
        lonNLL = float((lines[6].split(' ')[14])) 
        profNLL= float((lines[6].split(' ')[16])[:-2] )
    evsel['profundidad_abs']=evsel.profundidad.iloc[0]-voldf.nref.iloc[0]/1000
    evHypo71 = evsel
    subprocess.run(['LocSum','./loc/'+str(idev)+'.sum.grid0.loc','1','./loc/'+str(idev),'./loc/'+str(idev)+'.*.*.grid0.loc']) # EJECUTA LocSum
    subprocess.run(['Grid2GMT',outdir_Vel2Grid_input,'./loc/'+str(idev),'./gmt','L','S']) # EJECUTA LocSum
    print('Hypo71    : Latitud: '+str(float(evHypo71.latitud.iloc[0]))+' , Longitud: '+str(float(evHypo71.longitud.iloc[0]))+', Profundidad: '+str(float(evHypo71.profundidad_abs.iloc[0]))+' km')
    print('NonLinLoc : Latitud: '+str(latNLL)+' , Longitud: '+str(lonNLL)+', Profundidad: '+str(profNLL)+' km')
    file='gmt'+str(idev)+'.LS.gmt'
    if os.path.isfile(file):
        os.remove(file)
    hypo=([evHypo71.longitud.iloc[0],evHypo71.latitud.iloc[0],evHypo71.profundidad_abs.iloc[0],
             evHypo71.erh.iloc[0],evHypo71.erz.iloc[0]])
    NLL=[lonNLL,latNLL,profNLL]
    copiar = 'cp ./loc/'+str(idev)+'.hyp '+ './saved_locs/'+str(idev)+'.hyp'
    copiar_red = 'cp ./loc/'+str(idev)+'.hyp '+ '/mnt/puntocientodos/tmp/pyNLL/'+str(idev)+'.hyp'
    os.system(copiar)
    os.system(copiar_red)
    plot_results_comparation(voldf,hypo,NLL,evsel,str(evento.idevento.iloc[0]))
    return voldf,hypo,NLL,evsel,str(evento.idevento.iloc[0])
