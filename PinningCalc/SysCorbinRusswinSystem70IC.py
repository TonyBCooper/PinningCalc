# -*- coding: utf-8 -*-
"""
@author: Tony Cooper
Created On: 2020-12-28
"""
from data import data
from SysBase import *
from tkinter.ttk import Label
from UIBase import UIBase, UISFIC

class SysCorbinRusswinSystem70IC(SysBase):

  def validateKeys(self):
    res = super().validateKeys()
    tmk = self.findFirst(KeyType.TMK)
    con = self.findFirst(KeyType.Control)
    if (con == None):
      return False
    if (tmk == None):
      con.errorMessage = 'TMK required'
      return False
    if (con.errorMessage != None):
      return False
    if (con.cuts[0] != tmk.cuts[0]):
      con.errorMessage = 'First cut must match TMK'
      return False
    if (con.cuts[-1] != tmk.cuts[-1]):
      con.errorMessage = 'Last cut must match TMK'
      return False
    return res

  def bitsToPinning(self, bits:list)->PinningChart:
    pc = super().bitsToPinning(bits)
    if (not isinstance(pc, PinningChart)):
      return pc
    row:PinRow=None
    rowControl:PinRow=None
    rowTop:PinRow=None
    for row in pc.rows:
      if (row.PinRowType == PinRowType.Driver):
        row.pins[0] = None
        row.pins[5] = None
        row.pinText[0] = 'T'
        row.pinText[5] = 'T'
        rowTop = row
      elif (row.PinRowType == PinRowType.Control):
        row.pins[0] = None
        row.pins[5] = None
        row.pinText[0] = ' '
        row.pinText[5] = ' '
        rowControl = row
    if (rowControl == None):
      return 'Missing Control Row'
    if (rowTop == None):
      return 'Missing Top Row'

    keyControl = self.findFirst(KeyType.Control)
    if (keyControl == None):
      return 'Missing a Control Key'
    
    for x in range(1,4+1):
      tot = 0
      rowTop.pinText[x] = keyControl.cuts[x]
      rowTop.pins[x] = int(rowTop.pinText[x])
      for row in pc.rows:
        if ((row != rowControl) and (row != rowTop)):
          tot += row.pins[x] or 0
          if (row.PinRowType == PinRowType.Bottom):
            tot += 1
      rowControl.pins[x] = rowTop.pins[x] - tot
      rowControl.pinText[x] = str(rowControl.pins[x]) if (rowControl.pins[x] <=0) else '+'+str(rowControl.pins[x])

    return pc

class UICorbinRusswinSystem70IC(UISFIC):

  def Save(self):
    pass

  def Load(self):
    pass

  def CreateSetup(self, master):
    return Label(master, text="").grid(column=0, row=0)

SysBase.RegisterClass(SysCorbinRusswinSystem70IC, 'Sys70IC')
UIBase.RegisterUI('Sys70IC',UICorbinRusswinSystem70IC)