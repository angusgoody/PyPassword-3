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

#====================Variables====================
mainFrame.windowColour=window.cget("bg")

#====================User Interface====================

#======Status and context======
#region status/context

#Status variables
statusVar=StringVar()
statusVar.set("Home")
#Set screen variable up
screen.statusVar=statusVar
#Create the label for status
statusBar=mainLabel(window,textvariable=statusVar,font="Avenir_Bold 15")
#Display the bar
statusBar.colour("#24544C")
statusBar.pack(side=BOTTOM,fill=X)

#Initiate the context bar for the whole program
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
splashScreen.addContextInfo(0,text="View Log",enabledColour="#17F388",
                            hoverColour="#13C770",clickedColour="#41F59D")
#View Log
splashScreen.addContextInfo(1,text="Go to pods",enabledColour="#A5F413",
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
loginScreen.addContextInfo(0,text="Back")
loginScreen.addContextInfo(1,text="Unlock",enabledColour="#B1F62D")
loginScreen.addContextInfo(2,text="Show Hint")

#Center
loginSub=mainFrame(loginScreen)
loginSub.pack(expand=True,fill=X,padx=20)


#Label for current file
loginFileVar=StringVar()
loginFileVar.set("No file loaded")
loginFileLabel=mainLabel(loginSub,textvariable=loginFileVar,font="Avenir 30")
loginFileLabel.pack(pady=10)

#Entry to enter password
loginEntry=advancedEntry(loginSub,"Enter Password",font="Avenir 20",justify=CENTER)
loginEntry.pack(fill=X)


#Label for telling user if password is correct etc
loginAttemptVar=StringVar()
loginAttemptLabel=mainLabel(loginSub, textvariable=loginAttemptVar, font="Avenir 15")
loginAttemptLabel.pack(pady=10)

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
openScreen.addContextInfo(1,text="Open",enabledColour="#2EE697")
openScreen.addContextInfo(2,text="Open Other")



#Listbox
openListbox=advancedListbox(openScreen)
openListbox.pack(expand=True,fill=BOTH)

#endregion
#====================Functions====================

#======Splash Screen========
def exit():
	"""
	This procedure is the
	exit command and is run when
	the program needs to end. Any
	saves etc are done here
	"""

	#Destroy the window
	window.destroy()
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
            masterPodInstance=loadMasterPodFromFile(file)
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

def loadMasterPodToLogin():
	"""
	This function will
	load a master pod from 
	the open screen and send
	it to the login screen
	"""
	#Get from listbox
	currentSelection=openListbox.getSelection()
	#Check if there is something selected that is valid
	if type(currentSelection) == masterPod:

		#Set the selected pod variable to the selected object
		masterPod.currentMasterPod=currentSelection
		#Show the screen
		loginScreen.show()
	else:
		showMessage("Select Pod","Please select a master pod")

#======Login Screen========

def showHint():
	"""
	This function will display
	the hint of the currently loaded
	master pod and show it on the label
	underneath the entry
	"""
	#First get the master pod
	currentMasterPod=masterPod.currentMasterPod
	#Get the hint
	hint=currentMasterPod.hint
	#Update the control variable
	loginAttemptVar.set(hint)

def attemptMasterPodUnlock():
	"""
	This function gets the user input
	from the entry and attempts to unlock 
	the currently loaded master pod.
	"""
	#Get the data from the entry
	attempt=loginEntry.getData()
	#Check the user entered something
	if attempt:
		#Check the password
		unlockAttempt=checkMasterPodPassword(masterPod.currentMasterPod,attempt)

	else:
		showMessage("Enter","Please enter password")
#====================Button commands====================

#Splash Screen
splashScreen.updateCommand(1,command=lambda: openScreen.show())
splashScreen.updateCommand(2,command=lambda: exit())
#Open Screen
openScreen.updateCommand(1,command=lambda: loadMasterPodToLogin())
#Login Screen
loginScreen.updateCommand(0,command=lambda: openScreen.show())
loginScreen.updateCommand(2,command=lambda: showHint())
loginScreen.updateCommand(1,command=lambda: attemptMasterPodUnlock())
#====================Screen commands====================
#Login Screen
loginScreen.addScreenCommand(lambda: loginScreen.colour(mainFrame.windowColour))
loginScreen.addScreenCommand(lambda: loginAttemptVar.set(""))
loginScreen.addScreenCommand(lambda: loginFileVar.set(masterPod.currentMasterPod.masterName))
#====================Bindings====================
#Status
recursiveBind(statusBar,"<Double-Button-1>",lambda event: goHome())
#Open Screen
recursiveBind(openListbox,"<Double-Button-1>",lambda event: loadMasterPodToLogin())
recursiveBind(openListbox,"<Button-1>",lambda event: openScreen.updateCommand(1,state=True))

#====================Testing Area====================

#====================Initial Loaders====================

runCommand(splashScreen.show())
runCommand(findMasterPods(getWorkingDirectory()))
#====================END====================
window.mainloop()

