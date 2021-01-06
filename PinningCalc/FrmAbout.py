# -*- coding: utf-8 -*-
"""
@author: Tony Cooper
Created On: 2020-12-28
"""

from tkinter import Toplevel, PhotoImage, Canvas
from tkinter.ttk import Frame, Label, LabelFrame, Button, Style, Scrollbar
import os
import pkg_resources
import sys
#from PIL import Image

class FrmAbout(Toplevel):
  frm:Frame = None
  btnOk:Button = None
  img: PhotoImage = None

  def __init__(self, parent):
    super().__init__(parent)
    self.frm = Frame(self)
    self.frm.grid(column=0, row=0, sticky='news')
    Label(self.frm, text='Pinning Calc', font=('size',24)).grid(row=0, pady=(16,0), padx=16)
    imgName = 'app.png' if (sys.platform != 'darwin') else 'app.gif'
    img = PhotoImage(data=pkg_resources.resource_stream(__name__, imgName).read())
    self.img = img.subsample(4)
    Label(self.frm, image=self.img).grid(row=1, pady=(0,16), padx=16)

    statement = 'The Lock Pinning Calculator app was created in the hope that it would be of use to locksmiths around the world'
    Label(self.frm, text=statement, wraplength=300, justify='center').grid(row=2, pady=16, padx=16)

    lbl = Label(self.frm, text='Contributions By:', font=('size',10), foreground='blue')
    frame = LabelFrame(self.frm, borderwidth=5, labelwidget=lbl)
    frame.grid(row=3, padx=16, pady=16)
    Label(frame, text='Tony Cooper').grid(column=0, row=0, pady=5, padx=5)
    Label(frame, text='tony@balsa.co.nz').grid(column=1, row=0, pady=5, padx=5)

    self.btnOk = Button(self.frm, text='OK', command=self.destroy)
    self.btnOk.grid(column=0, row=4, pady=16, padx=16)

