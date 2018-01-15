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
mainVars["window"]=window
#====================Menus====================

#Menu when locked
publicMenu=Menu(window)
mainVars["publicMenu"]=publicMenu

#Menu inside the program
privateMenu=Menu(window)
mainVars["privateMenu"]=publicMenu

#Update the screen class menus
screen.publicMenu=publicMenu
screen.privateMenu=privateMenu

#====================Log====================
log=logClass("Main")
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
mainVars["context"]=context

#endregion
#======Splash Screen======
#region splash

#Create screen using screen class
splashScreen=screen(window,"PyPassword")

#Setup Context bar
splashScreen.context=context
#Go to pods
splashScreen.addContextInfo(0,text="View Log",enabledColour=mainBlueColour,
                            hoverColour=mainSecondBlueColour,clickedColour=mainClickedColour)
#View Log
splashScreen.addContextInfo(1,text="Go to pods",enabledColour=mainGreenColour,
                            hoverColour=mainSecondGreenColour,clickedColour=mainClickedColour)
#Exit
splashScreen.addContextInfo(2,text="Exit",enabledColour=mainRedColour,
                            hoverColour=mainSecondRedColour,clickedColour=mainClickedColour)

#Create centered frame for logo
splashCenter=mainFrame(splashScreen)
splashCenter.pack(expand=True)

#Get the logo for PyPassword and create image label
splashImage=getPicture("PyPassword 3 logo.gif")
splashLabel=Label(splashCenter,image=splashImage)
splashLabel.pack()

#Create the title
splashTitle=mainLabel(splashCenter,text="PyPassword",font="Avenir 39",fg=mainBlueColour)
splashTitle.pack()

#Colour the splash screen
#splashScreen.colour("#24544C")

#endregion
#======Login Screen======
#region Login
loginScreen=screen(window,"Login")

#Context
loginScreen.context=context
loginScreen.addContextInfo(2,text="Back")
loginScreen.addContextInfo(1,text="Unlock",enabledColour=mainGreenColour)
loginScreen.addContextInfo(0,text="Show Hint")

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
loginAttemptNumberVar=IntVar()
loginAttemptLabel=mainLabel(loginSub, textvariable=loginAttemptVar, font="Avenir 17")
loginAttemptLabel.pack(pady=10)

#endregion
#======Open Screen======
#region Open
openScreen=screen(window,"Open")
openScreen.colour("#ADDCFC")

#Top label
openTopLabel=topLabel(openScreen,text="Select Master Pod")
openTopLabel.pack(side=TOP,fill=X)

#Context
openScreen.context=context
openScreen.addContextInfo(0,text="Create New")
openScreen.addContextInfo(1,text="Open",enabledColour=mainBlueColour)
openScreen.addContextInfo(2,text="Open Other")

#Listbox
openListbox=advancedListbox(openScreen,font="Avenir 37")
openListbox.pack(expand=True,fill=BOTH)

#endregion
#======Pod Screen======
#region podScreen

#Initiate screen
podScreen=screen(window,"View Pods",protected=True)
podScreen.context=context

#Create a label along top of screen
podTopVar=StringVar()
podTopVar.set("Select a pod")
podTopLabel=topLabel(podScreen,textvariable=podTopVar)
podTopLabel.pack(side=TOP,fill=X)

#Create the listbox
podListbox=advancedListbox(podScreen,font="Avenir 25")
podListbox.pack(expand=True,fill=BOTH)

#Create the context buttons
podScreen.addContextInfo(0,text="New Pod",enabledColour=mainBlueColour)
podScreen.addContextInfo(1,text="Open Pod",enabledColour=mainGreenColour)
podScreen.addContextInfo(2,text="Exit Pod",enabledColour=mainRedColour)

#endregion
#======View Pod Screen======
#region viewPod
viewPodScreen=screen(window,"View Pod",protected=True)
viewPodScreen.context=context

#Create the context buttons
viewPodScreen.addContextInfo(0,text="Delete",clickedColour=mainRedColour)
viewPodScreen.addContextInfo(1,text="Edit",enabledColour=mainBlueColour)
viewPodScreen.addContextInfo(2,text="Back")

#Top Label
viewPodLabelVar=StringVar()
viewPodLabelVar.set("Pod")

viewPodLabel=topLabel(viewPodScreen,textvariable=viewPodLabelVar)
viewPodLabel.pack(side=TOP,fill=X)

#Notebook
viewPodNotebook=podNotebook(viewPodScreen)
viewPodNotebook.pack(expand=True,fill=BOTH)

#endregion
#====================Functions====================


#======System functions========

def saveLogs():
	"""
	This function will save the log files
	to the correct location before
	exiting the program
	"""
	print("Saving logs...")
	for log in logClass.logs:
		logClass.logs[log].saveLog()
		print("Saved:",log)

def closeProgram():
	"""
	This is the function that is called
	when the user clicks to exit the 
	program
	"""
	#Save logs
	try:
		saveLogs()
	except Exception as e:
		print("Error saving logs because..",e)
		#Exit even if error saving logs
		window.destroy()
	else:
		#Exit the program
		window.destroy()
#======Splash Screen========

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
		podScreen.show()
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
		#Check if the masterPod is locked
		if hasattr(currentSelection,"locked"):
			if type(currentSelection.locked) is datetime:
				if currentSelection.locked > getCurrentTime():
					loginAttemptVar.set("Master pod has been locked")
					loginScreen.colour("#6251B3")
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

		if unlockAttempt == True:
			#Password was correct
			loginAttemptVar.set("Access Granted")
			#Colour the screen a green for correct
			loginScreen.colour(mainGreenColour)
			#Reset the attempt var
			loginAttemptNumberVar.set(0)

			#----Any view pod setup here---

			#Take user to the pod screen
			podScreen.show()
			#Update the variable
			podTopVar.set(masterPod.currentMasterPod.masterName+" Accounts")

		else:
			if unlockAttempt == "locked":
				loginAttemptVar.set("Master pod has been locked")
				loginScreen.colour("#6251B3")
				#Should go last because processes will freeze
				showMessage("Locked","This master pod is locked for 5 minutes")

			else:
				#Add one to the attempt counter
				loginAttemptNumberVar.set(loginAttemptNumberVar.get()+1)
				#The password was incorrect
				loginAttemptVar.set("Incorrect Password "+"("+str(loginAttemptNumberVar.get())+")")
				#Colour the screen incorrect colour
				loginScreen.colour(mainRedColour)

			addDataToWidget(loginEntry,"")

	else:
		showMessage("Enter","Please enter password")

#======Pod Screen========

def loadPodsToScreen():
	"""
	This function will load the pods in
	the master pod to the screen.
	"""
	#Get current master pod
	currentMasterPod=masterPod.currentMasterPod
	#Clear the listbox
	podListbox.secureClear()
	#Add to listbox
	for pod in currentMasterPod.peas:

		#Get the actual pod
		podInstance=currentMasterPod.peas[pod]

		#Generate a colour in case no colour is found
		podColour=generateHexColour()

		#Get the template for the pod
		podTemplateType=podInstance.templateType

		#Attempt to find the template colour
		if podTemplateType in podTemplate.templateColours:
			podColour=podTemplate.templateColours[podTemplateType]

		#Add to listbox
		podListbox.addObject(pod,podInstance,colour=podColour)

def openPod():
	"""
	This function is run
	when user double clicks
	on a pod in the listbox
	"""
	selectedPod=podListbox.getSelection()
	#Check something was selected
	if selectedPod:
		#Get the template type of the pod
		podType=selectedPod.templateType
		#Load the view pod screen
		viewPodScreen.show()
		#Load the notebook with a template type
		viewPodNotebook.loadTemplate(podType)
		#Update the variable
		masterPod.currentMasterPod.currentPeaPod=selectedPod
		#Update the top bar on the view pod screen
		viewPodLabelVar.set(selectedPod.peaName)
		#Add the pod data to screen
		viewPodNotebook.addPodData(selectedPod)
		#Then disable the screen for read only
		viewPodNotebook.changeNotebookState(True)

def exitPod():
	"""
	This is called when the
	user wants to exit a pod.
	The pod is secured and saved
	"""
	#Save
	masterPod.currentMasterPod.save()
	#Remove the key from box
	del keyBox.keyHoles[masterPod.currentMasterPod]
	#Show the correct frame
	openScreen.show()

def createNewPeaPod():
	"""
	Function to create a new pea
	pod inside a master pod
	"""
	newWindow=dataWindow(window,"Create Pea Pod")
	#Add the status bar
	#Add the context buttons
	newWindow.context.addButton(0,text="Cancel",enabledColour=mainRedColour)
	newWindow.context.addButton(1,text="Create",enabledColour=mainBlueColour)



#====================Button commands====================

#Splash Screen
splashScreen.updateCommand(1,command=lambda: openScreen.show())
splashScreen.updateCommand(2,command=lambda: closeProgram())
#Open Screen
openScreen.updateCommand(1,command=lambda: loadMasterPodToLogin())
#Login Screen
loginScreen.updateCommand(2,command=lambda: openScreen.show())
loginScreen.updateCommand(0,command=lambda: showHint())
loginScreen.updateCommand(1,command=lambda: attemptMasterPodUnlock())
#Pod screen
podScreen.updateCommand(0,command=createNewPeaPod)
podScreen.updateCommand(2,command=lambda: exitPod())
podScreen.updateCommand(1,command=lambda: openPod())
#View Pod screen
viewPodScreen.updateCommand(2,command=lambda: podScreen.show())
viewPodScreen.updateCommand(1,command=lambda: viewPodNotebook.startEdit())

#====================Screen commands====================
#Login Screen
loginScreen.addScreenCommand(lambda: loginAttemptNumberVar.set(0))
loginScreen.addScreenCommand(lambda: loginEntry.resetEntry())
loginScreen.addScreenCommand(lambda: loginScreen.colour(mainFrame.windowColour))
loginScreen.addScreenCommand(lambda: loginAttemptVar.set(""))
loginScreen.addScreenCommand(lambda: loginFileVar.set(masterPod.currentMasterPod.masterName))
#Pod Screen
podScreen.addScreenCommand(lambda: loadPodsToScreen())

#====================Bindings====================
#System
window.protocol('WM_DELETE_WINDOW', lambda: closeProgram())

recursiveBind(statusBar,"<Double-Button-1>",lambda event: goHome())
#Open Screen
recursiveBind(openListbox,"<Double-Button-1>",lambda event: loadMasterPodToLogin())
recursiveBind(openListbox,"<Button-1>",lambda event: openScreen.updateCommand(1,state=True))
#Login Screen
recursiveBind(loginEntry,"<Return>",lambda event: attemptMasterPodUnlock())
#Pod screen
recursiveBind(podListbox,"<Double-Button-1>",lambda event: openPod())
#====================Testing Area====================

#====================Initial Loaders====================

runCommand(lambda: splashScreen.show(),name="Splash loader")
runCommand(lambda: findMasterPods(getWorkingDirectory()),name="Finding master pods")
#====================END====================

window.mainloop()

