#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 15:00:09 2022

@author: sergio
"""

import sys
sys.path.append('/mnt/puntodiez/pyovdas_lib/')
import pandas as pd
import ovdas_getfromdb_lib as gdb
pd.options.mode.chained_assignment = None  # default='warn'

aer = gdb.extraer_eventos('2021-01-01','2022-01-01',volcan='NevChillan')

aer = pd.DataFrame(aer)
aer = aer[aer.ml>2]
aer = aer[aer.nestaciones>8]
aer = aer[aer.gap<180]