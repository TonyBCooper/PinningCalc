# -*- coding: utf-8 -*-
"""
@author: Tony Cooper
Created On: 2020-12-28
"""

from data import *

class PinRowType:
  Bottom = 'Bottom'
  Master = 'Master'
  Driver = 'Driver'
  Control = 'Control'

class KeyType:
  TMK = 'TMK'
  Control = 'Control'
  ChangeKey = 'ChangeKey'

class Key:
  keyType:str = KeyType.ChangeKey
  cuts:str = None
  errorMessage:str = None

class PinRow:
  PinRowType:str = None
  pins:list = None
  pinText:list = None
  
  def __init__(self, PinRowType:str, numChambers:int):
    self.PinRowType = PinRowType
    self.pins = [None] * numChambers
    self.pinText = [None] * numChambers

class PinningChart:
  rows:list = None #list of PinRow

  def __init__(self):
    self.rows = []

  def toString(self):
    res = ''
    if (self.rows == None):
      return 'No Pinning'
    for row in self.rows:
      line = row.PinRowType.ljust(7, ' ')
      for value in row.pinText:
        value = value or '.'
        line += value.rjust(3,' ')
      res += line + "\n"
    return res

class SysBase:
  isIC:bool = None
  systemType:SystemType = None
  keys:list = [] #Key
  _classes = {}

  def __init__(self, systemType:SystemType):
    self.systemType = systemType
    self.isIC = systemType.controlSleeve != None

  def addCuts(self, cuts:str, bits:list, isIC: bool)->bool:
    if (len(cuts) != self.systemType.chamberCount):
      return False
    i = 0
    for c in cuts:
      n = self.systemType.mapSymbolToDepth.get(c)
      if (n == None):
        return False
      if (isIC):
        n += self.systemType.controlSleeve
      n = 1 << n
      bits[i] = bits[i] | n
      i += 1
    return True
  
  def validateKeys(self):
    res = True
    for key in self.keys:
      key.errorMessage = None
      cuts = key.cuts
      if (len(cuts) < self.systemType.chamberCount):
        key.errorMessage = 'Too few cuts'
        res = False
      elif (len(cuts) > self.systemType.chamberCount):
        key.errorMessage = 'Too many cuts'
        res = False
      else:
        for c in cuts:
          if (self.systemType.mapSymbolToDepth.get(c) == None):
            key.errorMessage = 'Invalid cut'
            res = False
    return res

  def bitsToPinning(self, bits:list)->PinningChart:
    res = PinningChart()
    stack = self.systemType.stackHeight or len(self.systemType.cutSymbols)
    pins = [None] * self.systemType.chamberCount
    for i in range(0, len(pins)):
      pins[i] = []

    #Calc pin sizes
    x = 0
    for col in pins:
      pinSize = 0
      tot = 0
      n = bits[x]
      for y in range(0, stack):
        mask = 1 << y
        if ((mask & n) == mask):
          col.append(pinSize)
          tot += pinSize
          pinSize = 1
        else:
          pinSize += 1
      if (tot < stack):
        col.append(stack - tot)
      x += 1

    #Get Bottom Pins
    rowBottom = PinRow(PinRowType.Bottom, self.systemType.chamberCount)
    for x in range(0, self.systemType.chamberCount):
      col = pins[x]
      n = col.pop(0)
      rowBottom.pins[x] = n
      rowBottom.pinText[x] = self.systemType.mapDepthToSymbol.get(n) or '?'

    #Get Top Pins
    rowTop = PinRow(PinRowType.Driver, self.systemType.chamberCount)
    for x in range(0, self.systemType.chamberCount):
      col = pins[x]
      if (len(col) > 0):
        n = col.pop()
        rowTop.pins[x] = n
        rowTop.pinText[x] = str(n) or '?'

    #Get Control Pins
    rowControl = PinRow(PinRowType.Control, self.systemType.chamberCount)
    if (self.systemType.controlSleeve != None):
      for x in range(0, self.systemType.chamberCount):
        col = pins[x]
        if (len(col) > 0):
          n = col.pop()
          rowControl.pins[x] = n
          rowControl.pinText[x] = str(n) or '?'
    
    #Get Masters
    b = True
    while(b):
      b = False
      row = PinRow(PinRowType.Master, self.systemType.chamberCount)
      for x in range(0, self.systemType.chamberCount):
        col = pins[x]
        if (len(col) > 0):
          b = True
          n = col.pop()
          row.pins[x] = n
          row.pinText[x] = str(n) or '?'
      if (b):
        res.rows.append(row)
    if (self.systemType.controlSleeve != None):
      res.rows.insert(0, rowControl)
      res.rows.insert(0, rowTop)
    elif (self.systemType.stackHeight != None):
      res.rows.insert(0, rowTop)
    res.rows.append(rowBottom)
    return res

  def Calc(self):
    bits = [0] * self.systemType.chamberCount
    if (len(self.keys) == 0):
      return '...'
    for key in self.keys:
      isControl = (key.keyType == KeyType.Control)
      if (not self.addCuts(key.cuts, bits, isControl)):
        return 'Invalid '+key.keyType
    return self.bitsToPinning(bits)

  def findFirst(self, keyType: str)->Key:
    for key in self.keys:
      if (key.keyType == keyType):
        return key

  @staticmethod
  def RegisterClass(TheClass, className:str):
    SysBase._classes[className] = TheClass

  @staticmethod
  def CreateClassFor(systemType: SystemType):
    tc = SysBase._classes.get(systemType.className)
    if (tc == None):
      raise Exception('Class for '+systemType.className+' not found')
    return tc(systemType)

class sysInline(SysBase):
  pass

SysBase.RegisterClass(sysInline, 'Inline')

class sysSFIC(SysBase):
  pass

SysBase.RegisterClass(sysSFIC, 'SFIC')