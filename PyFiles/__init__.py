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

frame=Frame(window)

recursiveBind(frame,"<Enter>","")

#====================User Interface====================

#======Status======

#====================END====================
window.mainloop()

