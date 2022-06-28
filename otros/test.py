#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 19 10:40:03 2022

@author: sismologia
"""

import subprocess


p=subprocess.Popen(['/opt/focmec/bin/focmec'],
                   stdin=subprocess.PIPE,
                   stdout=subprocess.PIPE)


p.stdin.write(b'oli\n')
p.stdin.write(b'algo\n')
p.stdin.write(b'FOCMEC.inp\n')
p.stdin.write(b'\n')
p.stdin.write(b'\n')
p.stdin.write(b'\n')
p.stdin.write(b'\n')
p.stdin.write(b'\n')
p.stdin.write(b'\n')
p.stdin.write(b'\n')
p.stdin.write(b'\n')
p.stdin.write(b'\n')
p.stdin.write(b'\n')
p.stdin.write(b'\n')
p.stdin.write(b'\n')
p.stdin.write(b'\n')
outputlog,errorlog = p.communicate()
p.stdin.close()

