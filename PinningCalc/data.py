# -*- coding: utf-8 -*-
"""
static class "data" acts as a singleton containing a list of possible System Types
At some point this would need to store user defined system types
@author: Tony Cooper
Created On: 2020-12-28
"""

class SystemType:
  id:int = None
  className:str = None
  name:str = None
  chamberCount:int = None
  cutSymbols:str = None
  stackHeight:int = None
  controlSleeve:int = None

  _lastSymbols:str = None
  _mapSymbolToDepth:dict = None
  _mapDepthToSymbol:dict = None

  def __init__(self, id:int, className:str, name:str, chamberCount:int, cutSymbols:str, stackHeight:int, controlSleeve:int):
    self.id = id
    self.name = name
    self.className = className
    self.chamberCount = chamberCount
    self.cutSymbols = cutSymbols
    self.stackHeight = stackHeight
    self.controlSleeve = controlSleeve

  def copy(self):
    return SystemType(self.id, self.className, self.name, self.chamberCount, self.cutSymbols, self.stackHeight, self.controlSleeve)

  def CheckMaps(self):
    if ((self._lastSymbols != self.cutSymbols) or (self._mapSymbolToDepth == None)):
      self._lastSymbols = self.cutSymbols
      self._mapSymbolToDepth = {}
      self._mapDepthToSymbol = {}
      for i in range(0, len(self.cutSymbols)):
        c = self.cutSymbols[i]
        self._mapSymbolToDepth[c] = i
        self._mapDepthToSymbol[i] = c

  @property
  def mapSymbolToDepth(self)->dict:
    self.CheckMaps()
    return self._mapSymbolToDepth
  
  @property
  def mapDepthToSymbol(self)->dict:
    self.CheckMaps()
    return self._mapDepthToSymbol

class data:
  labelWidth = 15
  
  systems = [
    SystemType(-1,'Inline','Arrow', 6, '0123456789', None, None),
    SystemType(-2,'Inline','Corbin/Russwin K Class',  5, '1234567', None, None),
    SystemType(-3,'Inline','Corbin/Russwin System 70', 6, '123456', None, None),
    SystemType(-4,'Sys70IC','Corbin/Russwin System 70 IC', 6, '123456', 14, 6),
    SystemType(-5,'Inline','Schlage 6Pin', 6, '0123456789', None, None),
    SystemType(-6,'Inline','Kwikset', 5, '1234567', None, None),
    SystemType(-7,'Inline','Lockwood Australia', 6, '0123456789A', None, None),
    SystemType(-8,'Inline','Ruko/Assa 600', 6, '987654321', None, None),
    SystemType(-9,'Inline','Sargent', 6, '0123456789', None, None),
    SystemType(-10,'SFIC','Best A2', 7, '0123456789', 23, 10),
    SystemType(-11,'SFIC','Best A3', 7, '0123456', 16, 7),
    SystemType(-12,'SFIC','Best A4', 7, '012345', 14, 6)
  ]

  @staticmethod
  def findSystemTypeByName(name:str)->SystemType:
    for sys in data.systems:
      if (sys.name == name):
        return sys
    return None

  @staticmethod
  def findSystemTypeById(id:int)->SystemType:
    for sys in data.systems:
      if (sys.id== id):
        return sys
    return None

