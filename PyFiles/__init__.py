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

#======Status and context======
#region status
statusVar=StringVar()
statusVar.set("Home")
statusBar=contextBar(window)
statusBar.pack(side=BOTTOM,fill=X)
statusBar.addButton(0,textvariable=statusVar,enabledColour="#134611",hoverColour="#134611")

context=contextBar(window)
context.pack(side=BOTTOM,fill=X)

#endregion
#======Login Screen======
#region Login
loginScreen=screen(window,"Login")

#Context
loginScreen.context=context

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
openScreen.context=context
openScreen.addContextInfo(0,text="Create New")
openScreen.addContextInfo(1,text="Open",enabledColour="#2EE697",command=lambda: loginScreen.show())
openScreen.addContextInfo(2,text="Open Other")



#Listbox
openListbox=advancedListbox(openScreen)
openListbox.pack(expand=True,fill=BOTH)

#endregion
#====================Functions====================

def addMasterPodToScreen(masterPodInstance):
    """
    This function will add a master pod
    class to the screen on the UI and 
    ensure it's in the loaded dictionary
    """
    if type(masterPodInstance) is masterPod:
        #Get the name to be displayed
        displayName=masterPodInstance.masterName
        #Check for master pod colour
        masterPodColour=masterPodInstance.masterColour
        #Add to listbox
        openListbox.addObject(displayName,masterPodInstance,colour=masterPodColour)
        #Add to dictionary
        masterPod.loadedPods[displayName]=masterPodInstance

def findMasterPods(directory):
    """
    This function will find master pod
    files in a certain directory and 
    load them into the listbox 
    """
    files=findFiles(directory,".mp")
    if len(files) > 0:
        #Iterate
        for file in files:
            #Get master pod name
            displayName=getRootName(file)
            #Create instance
            masterPodInstance=loadMasterPod(file)
            #Add to listbox
            addMasterPodToScreen(masterPodInstance)

    else:
        log.report("No mp files found in directory")
        return None




#====================Bindings====================


#====================Testing Area====================

loginScreen.addContextInfo(0,enabledColour="#95EE9B",hoverColour="#9DFCA3",
                       clickedColour="#F951A3",text="Go back",command=lambda: openScreen.show())
loginScreen.addContextInfo(1,text="Place")
#====================Initial Loaders====================

openScreen.show()
findMasterPods(getWorkingDirectory())
#====================END====================
window.mainloop()

