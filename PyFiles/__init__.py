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
from PIL import Image, ImageTk

#====================Window====================
"""
This is where the basic window
is initiated and setup.
"""

window=Tk()
window.title("PyPassword 3")
window.geometry("400x300")




#====================User Interface====================

#======Status======
statusVar=StringVar()
statusVar.set("Home")
statusBar=contextBar(window)
statusBar.pack(side=BOTTOM,fill=X)
statusBar.addButton(0,textvariable=statusVar,enabledColour="#706EE6",hoverColour="#7A78FB")

#======Login Screen======
loginScreen=screen(window,"Login")
loginScreen.show()

loginSub=mainFrame(loginScreen)
loginSub.pack(expand=True,fill=X,padx=20)

loginEntry=Entry(loginSub,font="Avenir 20",show="•")
loginEntry.pack(fill=X)

#====================END====================
window.mainloop()

