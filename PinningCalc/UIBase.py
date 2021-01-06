# -*- coding: utf-8 -*-
"""
@author: Tony Cooper
Created On: 2020-12-28
"""

from SysBase import *
from data import *
from tkinter import *
from tkinter.ttk import *

class UIBase:
  UIs = {}
  sys:SysBase = None
  onChanged:callable = None

  def __init__(self, sys:SysBase):
    self.sys = sys

  @staticmethod
  def RegisterUI(className:str, ui):
    UIBase.UIs[className] = ui

  def Load(self):
    pass

  def Save(self):
    pass

  def handleChanged(self, event=None):
    if (self.onChanged != None):
      self.onChanged()

  def CreateSetup(self, master):
    return Label(master, text="Not Defined")

  def CreatePinningChart(self, master):
    return Label(master, text="Not Defined")

class UIInline(UIBase):
  _lblCutSymbols:Label = None
  _edtCutSumbols:Entry = None
  _lblNumberOfCuts:Label = None
  _cmbNumberOfCuts:Combobox = None
  _lblStackHeight:Label = None
  _cmbStackHeight:Combobox = None

  def Load(self):
    self._edtCutSumbols.delete(0, END)
    self._cmbNumberOfCuts.delete(0,END)
    self._cmbStackHeight.delete(0,END)
    if (self.sys == None):
      return
    st = self.sys.systemType
    self._edtCutSumbols.insert(0, st.cutSymbols)
    self._cmbNumberOfCuts.set(st.chamberCount)
    v = st.stackHeight if (st.stackHeight != None) else 'n/a'
    self._cmbStackHeight.set(v)
    
  def Save(self):
    if (self.sys == None):
      return
    st = self.sys.systemType
    st.cutSymbols = self._edtCutSumbols.get()
    st.chamberCount = int(self._cmbNumberOfCuts.get())
    v = self._cmbStackHeight.get()
    st.stackHeight = int(v) if (v.isnumeric()) else None

  def CreateSetup(self, master):
    pnl = Frame(master)
    pnl.grid(column=0, row=0)
    self._lblCutSymbols = Label(pnl, text="Cut Symbols:", width=data.labelWidth)
    self._lblCutSymbols.grid(column=0, row=0, sticky='w')
    self._edtCutSumbols = Entry(pnl, width=data.labelWidth)
    self._edtCutSumbols.grid(column=1, row=0, sticky='w')
    self._edtCutSumbols.bind('<KeyRelease>', self.handleChanged)

    self._lblNumberOfCuts = Label(pnl, text="Number of Cuts:",width=data.labelWidth)
    self._lblNumberOfCuts.grid(column=0, row=1, sticky='w')
    self._cmbNumberOfCuts = Combobox(pnl, state='readonly', values=list(range(3,10)), width=data.labelWidth)
    self._cmbNumberOfCuts.grid(column=1, row=1, sticky='w')
    self._cmbNumberOfCuts.bind('<<ComboboxSelected>>', self.handleChanged)

    self._lblStackHeight = Label(pnl, text="Stack Height:", width=data.labelWidth)
    self._lblStackHeight.grid(column=0, row=2, sticky='w')
    a = ['n/a'] + list(range(5,32))
    self._cmbStackHeight = Combobox(pnl, state='readonly', values=a, width=data.labelWidth)
    self._cmbStackHeight.grid(column=1, row=2, sticky='w')
    self._cmbStackHeight.bind('<<ComboboxSelected>>', self.handleChanged)
    return pnl

  def CreatePinningChart(self, master):
    pnl = Frame(master)
    pnl.grid(sticky='news')

    colours = ['#a0f0f0','#a0f0a0','#a0a0f0']

    pc = self.sys.Calc()
    if (isinstance(pc, PinningChart)):
      y=0
      row:PinRow = None
      for row in pc.rows:
        lbl = Label(pnl, text=row.PinRowType).grid(column=0, row=y, sticky='w')
        x=1
        for value in row.pinText:
          value = value or '.'
          bg = colours[x % 3]
          lbl = Label(pnl, text=value, justify=CENTER, anchor='n', width=4, background=bg)
          lbl.grid(column=x, row=y, sticky='ew')
          x += 1
        y += 1
    elif (isinstance(pc, str)):
      lbl = Label(pnl, text=pc)
      lbl.grid(sticky='news')
    else:
      lbl = Label(pnl, text='Waiting')
      lbl.grid(sticky='news')

    return pnl

class UISFIC(UIInline):
  _lblControlSleeve:Label = None
  _cmbControlSleeve:Combobox = None
  _intControlSleeve:IntVar = None

  def Load(self):
    super().Load()
    self._cmbControlSleeve.delete(0, END)
    if (self.sys == None):
      return
    self._intControlSleeve.set(self.sys.systemType.controlSleeve)

  def Save(self):
    super().Save()
    self.sys.systemType.controlSleeve = self._intControlSleeve.get()
  
  def CreateSetup(self, master):
    pnl = super().CreateSetup(master)
    self._lblControlSleeve = Label(pnl, text="Control Sleeve:", width=data.labelWidth)
    self._lblControlSleeve.grid(column=0, row=3, sticky='w')
    self._intControlSleeve = IntVar()
    self._cmbControlSleeve = Combobox(pnl, state='readonly', values=list(range(5,20)), width=data.labelWidth, textvariable=self._intControlSleeve)
    self._cmbControlSleeve.grid(column=1, row=3, sticky='w')
    self._cmbControlSleeve.bind('<<ComboboxSelected>>', self.handleChanged)
    return pnl

UIBase.RegisterUI('Inline', UIInline)
UIBase.RegisterUI('SFIC', UISFIC)
