#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 15:00:54 2022

@author: sergio
"""
year=2021       #year del evento
idev=10969145 #id del evento

#year=2021       #year del evento
#idev=1670 #id del evento
yNum=2000       #numero de celdas en horizontal
zNum=1050       #numero de celdas en vertical
gridsize=0.1    #tamaño de celda en km
VpVs = 1.78     #razón Vp/Vs
ro =2.7         #densidad promedio 
nerrores=0      #Numero de errores permitidos para FOCMEC
desvanglemax=40
signature='Sergi'
limpiar_carpetas=True





from lib.do_NLL import do_pyNLL
from lib.do_pyFOCMEC import do_pyFOCMEC
from lib.plot_both import plot_both
flag=0
try:
    [voldf,hypo,NLL,evsel,idevento] = do_pyNLL(idev, year, limpiar_carpetas, yNum, zNum, gridsize, VpVs, ro, signature)
    flag=flag+1
except:
    print('Evento No localizado =(')
            
#%%
#try:
do_pyFOCMEC(year, idev, nerrores,desvanglemax, evsel)
#                    flag=flag+1
#                except:
#                    print('Mecanismo de foco no calculado =(')
#                #%%
#                if flag==2:
#                    plot_both(voldf,hypo,NLL,evsel,idevento,year,idev,desvanglemax)
