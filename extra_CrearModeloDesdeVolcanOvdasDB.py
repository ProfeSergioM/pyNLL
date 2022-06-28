# -*- coding: utf-8 -*-
"""
Created on Wed Apr 28 09:50:02 2021

@author: sergio.morales
"""

volcan='Lanin'
vPvS=1.78
nombremod='lanin_prem' #USAR MINUSCULAS (LINUX)
from lib.crearModeloTaup import crearModeloTaup
crearModeloTaup(volcan,vPvS,nombremod)