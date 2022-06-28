#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 22 16:21:26 2021

@author: sergio.morales
"""
def prepare_folders(lista_carpetas,limpiar_carpetas):
    import shutil
    import os
    for folder in lista_carpetas:
        if not os.path.exists(folder):
            os.makedirs(folder)
        else:
            if limpiar_carpetas==True:
                shutil.rmtree(folder)
                os.makedirs(folder)