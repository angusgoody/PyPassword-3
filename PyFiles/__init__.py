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
window.geometry("570x450")




#====================User Interface====================

#======Status and context======
#region status
statusVar=StringVar()
statusVar.set("Home")
#Set screen variable up
screen.statusVar=statusVar
statusBar=mainLabel(window,textvariable=statusVar,font="Avenir_Bold 15")
statusBar.colour("#24544C")
statusBar.pack(side=BOTTOM,fill=X)

context=contextBar(window)
context.pack(side=BOTTOM,fill=X)

#endregion

#======Splash Screen======
#region splash

#Create screen using screen class
splashScreen=screen(window,"PyPassword")
#Setup Context bar
splashScreen.context=context
#Go to pods
splashScreen.addContextInfo(0,text="Go to pods",enabledColour="#17F388",
                            hoverColour="#13C770",clickedColour="#41F59D")
#View Log
splashScreen.addContextInfo(1,text="View Log",enabledColour="#A5F413",
                            hoverColour="#7CCE32",clickedColour="#B5F426")
#Exit
splashScreen.addContextInfo(2,text="Exit",enabledColour="#FFA500",
                            hoverColour="#E89600",clickedColour="#FFB52E")

#Create centered frame for logo
splashCenter=mainFrame(splashScreen)
splashCenter.pack(expand=True)

#Get the logo for PyPassword and create image label
splashImage=getPicture("PyPassword 3 logo.gif")
splashLabel=Label(splashCenter,image=splashImage)
splashLabel.pack()
#Create the title
splashTitle=mainLabel(splashCenter,text="PyPassword",font="Avenir 39",fg="#FFFFFF")
splashTitle.pack()
#Colour the splash screen
splashScreen.colour("#24544C")
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

#======Open Screen========
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

def goHome():
	"""
	This procedure will return to the home
	screen depending on what screen is currently
	loaded
	"""
	#Go to pod home
	if screen.lastScreen in screen.protectedScreens:
		pass
	else:
		splashScreen.show()



#====================Button commands====================
splashScreen.updateCommand(0,command=lambda: openScreen.show())
#====================Bindings====================
recursiveBind(statusBar,"<Double-Button-1>",lambda event: goHome())
#====================Testing Area====================

#====================Initial Loaders====================

runCommand(splashScreen.show())
runCommand(findMasterPods(getWorkingDirectory()))
#====================END====================
window.mainloop()

