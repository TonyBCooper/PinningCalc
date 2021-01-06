#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Tony Cooper
Created On: 2021-01-05
"""
import os
import py_compile
import shutil
import zipapp

sourceFiles = ['data', 'FrmAbout', 'FrmMain', 'SysBase', 'SysCorbinRusswinSystem70IC', 'UIBase']
copyFiles = ['__main__.py','app.icns', 'app.ico', 'app.png', 'app.gif']

d = os.path.dirname(__file__)
sourcePath = d+'/PinningCalc/'
targetPath = d+'/tmp/'

if (os.path.exists(targetPath)):
  shutil.rmtree(targetPath)
os.mkdir(targetPath)
os.mkdir(targetPath+'__pycache__')

for fn in sourceFiles:
  py_compile.compile(sourcePath+fn+'.py', cfile=targetPath+fn+'.pyc', optimize=2)
  shutil.copyfile(sourcePath+fn+'.py', targetPath+fn+'.py')

for fn in copyFiles:
  shutil.copyfile(sourcePath+fn, targetPath+fn)

zipapp.create_archive(d+'/tmp', d+'/PinningCalc.pyz', '/usr/bin/env python3')

shutil.rmtree(targetPath)