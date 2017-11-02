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

statusBar=contextBar(window)
statusBar.pack(side=BOTTOM,fill=X)


area=mainFrame(window)
area.pack(expand=True,fill=BOTH)

#Screens
screen1=screen(area,"Screen 1")
screen1.colour("#A9F955")
main=mainLabel(screen1,font="Avenir 25",text="Hi")
main.pack(expand=True)
screen2=screen(area,"Screen 2")
screen2.colour("#ADDCFC")
screen3=screen(area,"Screen 3")
screen3.colour("#F9D33A")




statusVar=StringVar()
statusVar.set("Home")
screen.statusVar=statusVar

statusBar.addButton(0,enabledColour="#B0F255",textvariable=statusVar,
                    hoverColour="#EDF1F7",clickedColour="#EDF1F7")
statusBar.addBinding("<Double-Button-1>",lambda event:temp())

newBar=contextBar(window,places=3,font="Avenir 15")
newBar.pack(side=BOTTOM,fill=X)

newBar.addButton(0,text="1",command=lambda: screen1.show())
newBar.addButton(1,text="2",enabledColour="#88E68D",command=lambda: screen2.show())
newBar.addButton(2,text="3",command=lambda: screen3.show())
#====================User Interface====================

#======Status======

#====================END====================
window.mainloop()

