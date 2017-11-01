# coding=utf-8

#Angus Goody
#12/10/17
#PyPassword 3 Main File

"""
This is the main file for PyPassword
3 and contains the core code to run
PyPassword 3
"""



#====================Imports====================
from tkinter import *
from tkinter import messagebox
from PyUi import *
from PEM import *
#====================Window====================
"""
This is where the basic window
is initiated and setup.
"""

window=Tk()
window.title("PyPassword 3")
window.geometry("400x300")

newBar=contextBar(window,places=3)
newBar.pack(side=BOTTOM,fill=X)

def temp():
	newBar.addButton(1,"REPLACEMENT",enabledColour="#D4AEF7")
newBar.addButton(0,"Custom",enabledColour="#E49373",command=temp)
newBar.addButton(1,"TEST",enabledColour="#87EFF7")
#====================User Interface====================

#======Status======

#====================END====================
window.mainloop()

