#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 22 17:15:10 2021

@author: sergio.morales
"""

def create_obs_input(evsel,tipo,randomint,df_sta):
    if tipo=='volcan':
        outdir_obs_input = './obs/'+str(evsel.idevento.iloc[0])+'.obs'
        import sys
        from datetime import datetime
        #import pandas as pd
        sys.path.append('//172.16.40.10/sismologia/pyovdas_lib/')
        import ovdas_getfromdb_lib as gdb
        fases = gdb.get_fasesLoc(evsel.idevento.iloc[0], evsel.fecha.iloc[0].year)
        file = open(outdir_obs_input, "w") 
        with open(outdir_obs_input, 'a') as the_file:
    
            for index,row in fases.iterrows():
                if row.fullstring is None:
                   polaridad=row.polaridad
                   if polaridad==" ":polaridad='?'
                   tiempop=datetime.fromtimestamp(row.tiempop)
                   fila = (row.cod[1:]+'Z ? ? '+row.tipoarribo.lower()+' P '+polaridad+' '+str(tiempop.year)+str(tiempop.month).zfill(2)+
                           str(tiempop.day).zfill(2)+' '+str(tiempop.hour).zfill(2)+str(tiempop.minute).zfill(2)+' '+
                           str(tiempop.second).zfill(2)+'.'+str(int(tiempop.microsecond/10000))+ " GAU 2.00e-02 "+
                          "-1.00e+00 -1.00e+00 -1.00e+00"
                           )
                   the_file.write(fila+'\n')
                   if row.tiempos>0:
                       tiempos=datetime.fromtimestamp(row.tiempos)
                       fila = (row.cod[1:]+'Z ? ? '+row.tipoarribo.lower()+' S ? '+str(tiempos.year)+str(tiempos.month).zfill(2)+
                               str(tiempos.day).zfill(2)+' '+str(tiempos.hour).zfill(2)+str(tiempos.minute).zfill(2)+' '+
                               str(tiempos.second).zfill(2)+'.'+str(int(tiempos.microsecond/10000))+ " GAU 2.00e-02 "+
                              "-1.00e+00 -1.00e+00 -1.00e+00"
                               )                   
                       the_file.write(fila+'\n')
                else:
                    polaridad=row.fullstring[6]
                    if polaridad==" ":polaridad='?'
                    fila = (row.fullstring[0:4]+" ? ? "+row.fullstring[4].lower()+" "+row.fullstring[5]+" "+polaridad+
                          ' 20'+row.fullstring[9:15]+" "+row.fullstring[15:19]+" "+row.fullstring[19:24]+ " GAU 2.00e-02 "+
                          "-1.00e+00 -1.00e+00 -1.00e+00")
                    the_file.write(fila+'\n')
                    if (row.fullstring[31:36]) !='00.00':
                        filas = (row.fullstring[0:4]+" ? ? "+row.fullstring[4].lower()+" "+row.fullstring[37]+" ? 20"+
                              row.fullstring[9:15]+" "+row.fullstring[15:19]+" "+row.fullstring[31:36]+ " GAU 4.00e-02 "+
                          "-1.00e+00 -1.00e+00 -1.00e+00")
                        the_file.write(filas+'\n')
                
                #the_file.write(row.fullstring+'\n')
            file.close()   
    elif tipo=='evento':
        from datetime import datetime,timedelta
        outdir_obs_input = './obs/'+randomint+'_syn.obs'
        file = open(outdir_obs_input, "w") 
        with open(outdir_obs_input, 'a') as the_file:
            for index,row in df_sta.iterrows():
                xday = datetime(2003,2,2)
                pxday = xday +timedelta(seconds=row.tP)
                pxdaystr = datetime.strftime(pxday, '%Y%m%d %H%M %S.%f')[:-4] 
                fila = (row.sta+'Z ? ? i P ? '+pxdaystr+' GAU 2.00e-02 -1.00e+00 -1.00e+00 -1.00e+00')
                the_file.write(fila+'\n')
                
                if row.faseS == True:
                    xday = datetime(2003,2,2)
                    sxday = xday +timedelta(seconds=row.tS)
                    sxdaystr = datetime.strftime(sxday, '%Y%m%d %H%M %S.%f')[:-4] 
                    fila = (row.sta+'Z ? ? i S ? '+sxdaystr+' GAU 2.00e-02 -1.00e+00 -1.00e+00 -1.00e+00')
                    the_file.write(fila+'\n')
        file.close()  