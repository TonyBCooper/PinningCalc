# -*- coding: utf-8 -*-
"""
Created on Fri Oct 16 13:41:31 2020

@author: Tony Cooper
"""

from tkinter import *
from tkinter.ttk import *
from tkinter.font import *
from data import *
from SysBase import *
from UIBase import *
from threading import Timer
import os
from FrmAbout import FrmAbout
import pkg_resources

class KeyInput:
  pnl:Frame = None
  lbl:Label = None
  edt:Entry = None
  lblError:Label = None
  btnDelete:Button = None
  key:Key = None

  def __init__(self, master, caption:str, onChanged, onDelete=None):
    self.pnl = Frame(master)
    self.pnl.grid(pady=(5,0))
    self.lbl = Label(self.pnl, text=caption, width=data.labelWidth)
    self.lbl.grid(column=0, row=0, sticky='nw', rowspan=2)
    self.edt = Entry(self.pnl, font=tkinter.font.nametofont('TkFixedFont'))
    self.edt.grid(column=1, row=0, sticky='w')
    if (onChanged != None):
      self.edt.bind('<KeyRelease>', onChanged)
    self.lblError = Label(self.pnl, foreground='red', font=('size', 8))
    self.lblError.grid(column=1,row=1)
    if (onDelete != None):
      self.btnDelete = Button(self.pnl, text='del', command=onDelete, width=5, style='del.TButton')
      self.btnDelete.grid(column=2, row=0, sticky='nw',rowspan=2, ipadx=0, ipady=0)
    self.key = Key()

  def setError(self, txt:str):
    self.lblError['text'] = txt if (txt != None) else ''

  def setRow(self, row):
    self.pnl.grid(column=0, row=row, sticky='w')

class FrmMain(Tk):
  _sys:SysBase = None
  _ui:UIBase = None
  _uiSettings:Widget = None
  _uiPinningChart:Widget = None

  _pnlPresets:LabelFrame = None
  _lblPresets:Label = None
  _cmbPresets:Combobox = None
  _pnlSettings:LabelFrame = None
  _pnlKeys:LabelFrame = None
  _pnlPinningChart:LabelFrame = None
  _pnlAdd:Frame = None
  _btnAdd:Button = None

  _inTMK:KeyInput = None
  _inControl:KeyInput = None
  _keys=[]
  _tmr:Timer = None

  menu:Menu = None

  def __init__(self):
    Tk.__init__(self)
    self.style = Style()
    lst = self.style.theme_names()
    if ('clam' in lst):
      self.style.theme_use('clam')
    self.style.configure('del.TButton', font=('size',8))
    self.style.configure('key.TEntry', font=('family','Courier', 'color','green'))
    self.style.configure('blue.TLabelFrame.Label', foreground='blue', font=('bold'))
    bg = self.style.lookup('TFrame','background')
    self.configure(bg=bg)
    self.minsize(600, 400)
    self.title('Pinning Calc')
    try:
      img = PhotoImage(data=pkg_resources.resource_stream(__name__, 'app.png').read())
      self.iconphoto(True, img)
    except:
      try:
        img = BitmapImage(data=pkg_resources.resource_stream(__name__, 'app.ico').read())
        self.iconphoto(True, img)
      except:
        try:
          img = BitmapImage(data=pkg_resources.resource_stream(__name__, 'app.icns').read())
          self.iconphoto(True, img)
        except:
          pass # Not impressed
      
    self.pnlPresets().grid(column=0, row=0, sticky='ew')
    lbl = Label(text='Setting', font=('size',10), foreground='blue')
    self._pnlSettings = LabelFrame(self, borderwidth=5, labelwidget=lbl)
    self._pnlSettings.grid(column=0, row=1, pady=10, sticky='ew')
    
    self.pnlKeys().grid(column=0, row=2, sticky='ew')

    lbl = Label(text='Pinning Chart', font=('size',10), foreground='blue')
    self._pnlPinningChart = LabelFrame(self, borderwidth=5, labelwidget=lbl)
    self._pnlPinningChart.grid(column=1, row=0, rowspan=3, padx=10, pady=10, sticky='n')

    self._pnlAdd = Frame(self).grid(column=0, row=3, sticky='ew')
    self._btnAdd = Button(self._pnlAdd, text='Add', command=self.addKey)
    self._btnAdd.grid(sticky='e')

    #Menu
    self.menu = Menu(self)
    self.configure(menu=self.menu)
    self.mnuFile = Menu(self.menu, tearoff=0)
    self.mnuFile.add_command(label='Exit', command=self.destroy)
    self.menu.add_cascade(label='File', menu=self.mnuFile)

    self.mnuHelp = Menu(self.menu, tearoff=0)
    self.menu.add_cascade(label='Help', menu=self.mnuHelp)
    self.mnuHelp.add_command(label='About', command=self.doHelpAbout)
  
  def PopulatePresets(self):
    a = []
    for sys in data.systems:
      a.append(sys.name)
    a.sort()
    self._cmbPresets['values'] = a

  def handlePresetSelected(self, event):
    if (self._uiSettings != None):
      self._uiSettings.destroy()
      self._uiSettings = None
    if (self._uiPinningChart != None):
      self._uiPinningChart.destroy()
      self._uiPinningChart = None
    st = data.findSystemTypeByName(self._cmbPresets.get())
    if (st == None):
      return
    self._sys = SysBase.CreateClassFor(st.copy())
    
    if (self._sys.isIC):
      if (self._inControl == None):
        self._inControl = KeyInput(self._pnlKeys, 'Control Key:', self.handleChange)
        self._inControl.setRow(1)
    else:
      if (self._inControl != None):
        self._inControl.pnl.destroy()
        self._inControl = None

    uiClass = UIBase.UIs[st.className]
    self._ui = uiClass(self._sys)
    self._uiSettings = self._ui.CreateSetup(self._pnlSettings)
    self._uiPinningChart = self._ui.CreatePinningChart(self._pnlPinningChart)
    self._ui.Load()
    self._ui.onChanged = self.handleChange
    self.handleChange()

  def pnlPresets(self):
    if (self._pnlPresets == None):
      lbl = Label(text='Presets', font=('size',10), foreground='blue')
      self._pnlPresets = LabelFrame(self, borderwidth=5, labelwidget=lbl)
      self._lblPresets = Label(self._pnlPresets, text="Preset:")
      self._lblPresets.grid(row=0, column=0, sticky='w')
      self._cmbPresets = Combobox(self._pnlPresets, state='readonly', width=30)
      self._cmbPresets.bind('<<ComboboxSelected>>', self.handlePresetSelected)
      self._cmbPresets.grid(column=0, row=0, sticky='ew')
      self.PopulatePresets()
    return self._pnlPresets

  def pnlKeys(self):
    if (self._pnlKeys == None):
      lbl = Label(text='Keys', font=('size',10), foreground='blue')
      self._pnlKeys = LabelFrame(self, borderwidth=5, labelwidget=lbl)
      self._inTMK = KeyInput(self._pnlKeys, 'Top Master Key:', self.handleChange)
      self._inTMK.setRow(0)
    return self._pnlKeys

  def ArrangeKeys(self):
    r = 2
    for itm in self._keys:
      itm.setRow(r)
      r += 1

  def addKey(self):
    key = KeyInput(self._pnlKeys, 'Key:', self.handleChange, lambda: self.delKey(key))
    self._keys.append(key)
    self.ArrangeKeys()
    self.handleChange()

  def delKey(self, key):
    self._keys.remove(key)
    key.pnl.destroy()
    self.ArrangeKeys()
    self.handleChange()
    
  def runit(self):
    
    def setit(ki:KeyInput, keyType:str):
      ki.key.keyType = keyType
      ki.key.cuts = ki.edt.get()
      ki.key.errorMessage = ''
      self._sys.keys.append(ki.key)

    #clear pinning chart
    if (self._uiPinningChart != None):
      self._uiPinningChart.destroy()
      self._uiPinningChart = None

    if (self._sys == None):
      return
    self._ui.Save()
    #Populate Keys
    self._sys.keys = []
    setit(self._inTMK, KeyType.TMK)
    if (self._inControl != None):
      setit(self._inControl, KeyType.Control)
    for itm in self._keys:
      setit(itm, KeyType.ChangeKey)
      itm.pnl.lift() #change tab order
    #Validate Keys
    res = self._sys.validateKeys()
    self._inTMK.setError(self._inTMK.key.errorMessage)
    if (self._inControl != None):
      self._inControl.setError(self._inControl.key.errorMessage)
    for itm in self._keys:
      itm.setError(itm.key.errorMessage)
    if (not res):
      return False

    #Calculate
    self._uiPinningChart = self._ui.CreatePinningChart(self._pnlPinningChart)

  def clearTimer(self):
    if (self._tmr == None):
      return
    self._tmr.cancel()
    self._tmr = None

  def startTimer(self):
    self.clearTimer()
    self._tmr = Timer(0.5, self.handleTimer)
    self._tmr.start()

  def handleTimer(self):
    self.clearTimer()
    self.runit()

  def handleChange(self, event=None):
    self.startTimer()
  
  def doHelpAbout(self):
    frm = FrmAbout(self)
    self.wait_window(frm)
