#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 28 14:14:58 2021

@author: sergio.morales
"""
modname = 'lanin_prem' #nombre de archivo del mod, ubicado en la carpeta "custom_inputs"
fasesname = 'Lanin_LAN_3syn' #nombre de archivo con estaciones y fases a genera
confname = 'conf_mod' #nombre de archivo con configuraciones
locname = 'loc_mod'

from lib.do_NLL_syn import do_pyNLL_syn
do_pyNLL_syn(modname,confname,fasesname,locname)