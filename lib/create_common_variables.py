#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 22 16:07:59 2021

@author: sergio.morales
"""
def create_common_variables(df,randomint,tipo):
    
    com_CONTROL = "CONTROL 1 "+randomint
    if tipo=='volcan':
        voldf=df
        com_TRANS = "TRANS AZIMUTHAL_EQUIDIST WGS-84 "+str(float(voldf.latitud.iloc[0]))+' '+str(float(voldf.longitud.iloc[0]))+' 0'
    elif tipo=='evento':
        com_TRANS = "TRANS AZIMUTHAL_EQUIDIST WGS-84 "+str(df[0])+' '+str(df[1])+' 0'
    return com_CONTROL,com_TRANS
    
