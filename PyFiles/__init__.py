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
#region Login
loginScreen=screen(window,"Login")
#loginScreen.show()

#Context
loginContext=contextBar(loginScreen,places=3)
loginContext.pack(side=BOTTOM,fill=X)

loginContext.addButton(1,enabledColour="#95EE9B",hoverColour="#9DFCA3",
                       clickedColour="#F951A3",text="Unlock")
#Center
loginSub=mainFrame(loginScreen)
loginSub.pack(expand=True,fill=X,padx=20)

loginEntry=Entry(loginSub,font="Avenir 20",show="•",justify=CENTER)
loginEntry.pack(fill=X)

loginVar=StringVar()
loginLabel=mainLabel(loginSub,textvariable=loginVar,font="Avenir 18")
loginLabel.pack(pady=10)

#endregion
#======Open Screen======
#region Open
openScreen=screen(window,"Open")
openScreen.colour("#ADDCFC")

#Top label
openTopLabel=topLabel(openScreen,text="Select Pod")
openTopLabel.pack(side=TOP,fill=X)

#Context
openContext=contextBar(openScreen,places=3)
openContext.pack(side=BOTTOM,fill=X)
#Context buttons
openContext.addButton(0,text="Create New")
openContext.addButton(1,text="Open",enabledColour="#2EE697")
openContext.addButton(2,text="Open Other")
#Listbox
openListbox=advancedListbox(openScreen)
openListbox.pack(expand=True,fill=BOTH)

#endregion
#====================Functions====================

def attempt():
	data=loginEntry.get()
	if data != "Harry":
		loginScreen.colour("#E68AAA")
		loginVar.set("Incorrect")
	else:
		loginScreen.colour("#95E68A")
		loginVar.set("Correct")

loginEntry.bind("<Return>",lambda event: attempt())

#====================Testing Area====================
openScreen.show()

#====================END====================
window.mainloop()

