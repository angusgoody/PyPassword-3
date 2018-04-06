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

from PyUi import *
from PEM import *
import random
import threading
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

#---------Menu setup--------

#Menu when locked
publicMenu=Menu(window)
mainVars["publicMenu"]=publicMenu

#Menu inside the program
privateMenu=Menu(window)
mainVars["privateMenu"]=privateMenu

#Update the screen class menus
screen.publicMenu=publicMenu
screen.privateMenu=privateMenu

#---------Menu Submenus--------

#Create private menus
privateFileMenu=Menu(privateMenu)
privatePasswordMenu=Menu(privateMenu)

#Public Menus
publicFileMenu=Menu(publicMenu)
#====================Threading controllers====================
mainThreadController=threadController("Main")

#====================Log====================
log=logClass("Main")
#====================Variables====================
mainFrame.windowColour=window.cget("bg")
#Boolean for processing the language for search
processLanguageOn=True

#Current type of password generator
currentGenPasswordMethod=StringVar()
currentReviewOrGen=StringVar()

#The current launched popup windows
currentPeaWindow=None
currentMasterWindow=None

#Store the currently loaded logs key=selection bar index value=directory
loadedLogs={}

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
loginEntry=advancedEntry(loginSub,"Enter Password",True,font="Avenir 20",justify=CENTER)
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
openTopLabel=topLabel(openScreen,text="Select or create Master Pod")
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

#Create the search bar
podSearchEntry=advancedEntry(podScreen,"Search",False,justify=CENTER,font="Avenir 14")
podSearchEntry.pack(fill=X,side=TOP)

#Search context
podSearchContext=contextBar(podScreen,places=2,font="Avenir 11")
podSearchContext.pack(fill=X,side=TOP)
#Create the listbox
podListbox=advancedListbox(podScreen,font="Avenir 25")
podListbox.pack(expand=True,fill=BOTH)

#Small context
podContext=contextBar(podScreen,font="Avenir 10",places=4)
podContext.pack(side=BOTTOM,fill=X)

podContext.addButton(0,text="Generate")
podContext.addButton(1,text="Review")
podContext.addButton(2,text="Audit")
podContext.addButton(3,text="View Key")

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
mainVars["podLabelVar"]=viewPodLabelVar
viewPodLabel=topLabel(viewPodScreen,textvariable=viewPodLabelVar)
viewPodLabel.pack(side=TOP,fill=X)

#Notebook
viewPodNotebook=podNotebook(viewPodScreen)
viewPodNotebook.pack(expand=True,fill=BOTH)

#endregion
#======Generate Password screen======
#region generate
genPasswordScreen=screen(window,"Generate",protected=True)
genPasswordScreen.context=context

#Context
genPasswordScreen.addContextInfo(0,text="Copy",enabledColour=mainBlueColour)
genPasswordScreen.addContextInfo(1,text="Regenerate",enabledColour=mainGreenColour)
genPasswordScreen.addContextInfo(2,text="Add to pod",enabledColour=mainPurpleColour)
genPasswordScreen.addContextInfo(3,text="Home",enabledColour=mainRedColour)

genPasswordNotebook=advancedNotebook(genPasswordScreen)
genPasswordNotebook.pack(fill=BOTH,expand=True)

genPasswordFrame=mainFrame(genPasswordNotebook)
genPasswordFrame.pack(fill=BOTH,expand=True)


genPasswordNotebook.addPage("Generate",genPasswordFrame)

#---Generate section---
genPasswordCenter=mainFrame(genPasswordFrame)
genPasswordCenter.pack(expand=True)

genPasswordVar=StringVar()
genPasswordVar.set("Password")
genPasswordLabel=mainLabel(genPasswordCenter,textvariable=genPasswordVar,font="Avenir 19",width=35)
genPasswordLabel.pack(fill=X,pady=5)

genPasswordStrengthVar=StringVar()
genPasswordStrengthLabel=mainLabel(genPasswordCenter,textvariable=genPasswordStrengthVar,font="Avenir 12")
genPasswordStrengthLabel.pack(pady=5)

#Notebook for characters or words
genPasswordCenterNotebook=advancedNotebook(genPasswordCenter)
genPasswordCenterNotebook.pack(expand=True,fill=BOTH)

#Characters
genPasswordCharFrame=mainFrame(genPasswordCenterNotebook)
genPasswordCharFrame.pack(pady=5)
genPasswordCenterNotebook.addPage("Characters", genPasswordCharFrame)

genPasswordCharLengthSlider=advancedSlider(genPasswordCharFrame, "Length", from_=7, to=50, value=random.randint(7, 50))
genPasswordCharLengthSlider.pack(fill=X)

genPasswordSymbolsSlider=advancedSlider(genPasswordCharFrame, "Symbols", from_=0, to=20, value=random.randint(0, 20))
genPasswordSymbolsSlider.pack(fill=X)

genPasswordDigitsSlider=advancedSlider(genPasswordCharFrame, "Digits", from_=0, to=20, value=random.randint(0, 20))
genPasswordDigitsSlider.pack(fill=X)

#Words
genPasswordWordsFrame=mainFrame(genPasswordCenterNotebook)
genPasswordCenterNotebook.addPage("Words",genPasswordWordsFrame)

genPasswordWordsLengthSlider=advancedSlider(genPasswordWordsFrame,"Number of words",from_=2, to=12,value=random.randint(2,12))
genPasswordWordsLengthSlider.pack(pady=5)

#Check button
genPasswordWordCommonVar=BooleanVar()
genPasswordWordsCommonCheckButton=Checkbutton(genPasswordWordsFrame,text="Non common words",variable=genPasswordWordCommonVar)
genPasswordWordsCommonCheckButton.pack()

#Seperator
genPasswordWordsSeperatorContainer=mainFrame(genPasswordWordsFrame)
genPasswordWordsSeperatorContainer.pack()

mainLabel(genPasswordWordsSeperatorContainer,text="Seperator",font="Avenir 13").pack(anchor=W,pady=6)

genPasswordWordsSeperatorVar=StringVar()
genPasswordWordsSeperatorVar.set("-")

genPasswordWordsHiphenChecked=Radiobutton(genPasswordWordsSeperatorContainer,text="Hiphen",variable=genPasswordWordsSeperatorVar,value=genPasswordWordsSeperatorVar.get())
genPasswordWordsHiphenChecked.pack(anchor=W)

genPasswordWordsStopChecked=Radiobutton(genPasswordWordsSeperatorContainer,text="Full stop",variable=genPasswordWordsSeperatorVar,value=".")
genPasswordWordsStopChecked.pack(anchor=W)

genPasswordUnderChecked=Radiobutton(genPasswordWordsSeperatorContainer,text="Underscore",variable=genPasswordWordsSeperatorVar,value="_")
genPasswordUnderChecked.pack(anchor=W)
genPasswordFrame.colour("#E7E7E7")

#---Review section---
genReviewFrame=mainFrame(genPasswordNotebook)
genPasswordNotebook.addPage("Review",genReviewFrame)

genReviewTopFrame=mainFrame(genReviewFrame)
genReviewTopFrame.pack(side=TOP,fill=X)
genReviewTopFrame.columnconfigure(0,weight=1)

genReviewEntry=Entry(genReviewTopFrame,font="Avenir 20",width=25,justify=CENTER)
genReviewEntry.grid(row=0,column=0,columnspan=2,sticky=EW)

genHideEntryVar=BooleanVar()
genHideEntryVar.set(False)
genReviewEntryToggleHide=Checkbutton(genReviewTopFrame,text="Hide",variable=genHideEntryVar,)
genReviewEntryToggleHide.grid(row=0,column=2,padx=10)

genReviewMainFrame=mainFrame(genReviewFrame)
genReviewMainFrame.pack(expand=True,fill=BOTH)

genReviewTree=advancedTree(genReviewMainFrame,["Field","Report"])
genReviewTree.pack(expand=True,fill=BOTH)

#Config the tree

genReviewTree.addSection("Field")
genReviewTree.addSection("Report")

genReviewTree.addTag("Pass", "#66CD84")
genReviewTree.addTag("Fail", "#ED4D79")

#endregion
#======Password screen======
#region passwordScreen
passwordScreen=screen(window,"Password data",protected=True)
passwordScreen.context=context

passwordScreen.addContextInfo(0,text="Copy",enabledColour=mainBlueColour)
passwordScreen.addContextInfo(1,text="Home",enabledColour=mainRedColour)

#Top
passwordTopFrame=mainFrame(passwordScreen)
passwordTopFrame.pack(side=TOP,fill=X)

passwordSearchEntry=advancedEntry(passwordTopFrame,"Search",False,font="Avenir 19",justify=CENTER)
passwordSearchEntry.pack(fill=X)

passwordScreenTopContext=contextBar(passwordTopFrame,places=1,font="Avenir 11")
passwordScreenTopContext.pack(fill=X)

passwordScreenTopContext.addButton(0,text="Clear",enabledColour="#D6DDDD")

#Middle
passwordMainFrame=mainFrame(passwordScreen)
passwordMainFrame.pack(fill=BOTH,expand=True)

passwordDataListbox=advancedListbox(passwordMainFrame,font="Avenir 20")
passwordDataListbox.pack(expand=True,fill=BOTH)

#endregion
#======Audit screen======
#region auditScreen
auditScreen=screen(window,"Audit",protected=True)
auditScreen.context=context

#Context
auditScreen.addContextInfo(0,text="Go Home",enabledColour=mainBlueColour)
#Configure weights
auditScreen.rowconfigure(2,weight=5)
auditScreen.columnconfigure(0,weight=3)

#Top section
auditTopSection=mainFrame(auditScreen)
auditTopSection.grid(row=0,column=0,columnspan=2,sticky=EW)

auditTopSectionSub=mainFrame(auditTopSection)
auditTopSectionSub.pack(expand=True)

auditTitleLabel=mainLabel(auditTopSectionSub,text="Your Security score..",font="Avenir 30")
auditTitleLabel.pack(pady=7)

auditScoreVar=StringVar()
auditScoreVar.set("0")
auditScoreLabel=mainLabel(auditTopSectionSub,textvariable=auditScoreVar,font="Helvetica 45",fg=mainRedColour)
auditScoreLabel.pack(pady=10)

#Table
auditTable=table(auditScreen,"Stats",True)
auditTable.grid(row=1,column=0,columnspan=2,sticky=EW)
auditTable.addRow("All accounts","0","#88D832")
auditTable.addRow("Strong Passwords","0","#88D832")
auditTable.addRow("Weak Passwords","0","#D86F76")
auditTable.addRow("Average Passwords","0","#D89F24")
auditTable.addRow("Duplicates","0","#D86F76")

#Results Tree
resultsTreeFrame=mainFrame(auditScreen)
resultsTreeFrame.grid(row=2,column=0,columnspan=2,rowspan=2,sticky=NSEW)

resultsTreeLabel=mainLabel(resultsTreeFrame,text="Pods",font="Avenir 27")
resultsTreeLabel.pack()

auditResultsTree=advancedTree(resultsTreeFrame,["Pod Name","Security"])
auditResultsTree.pack(expand=True,fill=BOTH)

#Add Tree Sections
auditResultsTree.addSection("Pod Name")
auditResultsTree.addSection("Security")

#Add Tree tags
auditResultsTree.addTag("Strong", "#66CD84")
auditResultsTree.addTag("Medium", "#EDC121")
auditResultsTree.addTag("Weak", "#ED4D79")
#endregion
#======Log screen======
#region logscreen
logScreen=screen(window,"Log")
logScreen.context=context

#Update context
logScreen.addContextInfo(0,text="Refresh",enabledColour=mainBlueColour)
logScreen.addContextInfo(1,text="Home",enabledColour=mainGreenColour)

#Log dictionary
logDict={"EncryptionLog":"Encryption",
 "MainLog":"Main",
 "User InterfaceLog":"Ui"}

#Create a bar
logSelectionBar=selectionBar(logScreen)
logSelectionBar.pack(side=TOP,fill=X)

logTree=advancedTree(logScreen,["Description","Time","Tag"])
logTree.pack(expand=True,fill=BOTH)

#Create the log tags
logTree.addTag("Error",mainRedColour)
logTree.addTag("Important",mainGreenColour)
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

def processSearchLanguage(dataField):
	"""
	This function will process the
	data from a data source and
	check for any natural language
	"""
	validCommands=["FILTER","TYPE","ORDER","SORT"]
	rawData=getDataFromWidget(dataField)
	#Split the data
	splitData=rawData.split("=")
	if len(splitData) > 1:
		command=splitData[0]
		commandData=splitData[1]
		if len(commandData.split()) > 0:
			commandName=str(command).upper()
			if commandName in validCommands:
				#Filter
				if commandName == "FILTER" or commandName == "TYPE":
					filterPodListbox(commandData)
				elif commandName == "ORDER" or commandName == "SORT":
					orderPodListbox(commandData)

#======Splash Screen========

#======Log Screen========

def showAllLogs():
	"""
	Will load all the logs
	:return:
	"""
	#Add sections to log screen
	allLogs=findFiles(getWorkingDirectory(),".log")
	counter=-1
	for l in allLogs:
		counter+=1
		base=getRootName(l)
		if base in logDict:
			base=logDict[base]
		#Add to selection bar
		logSelectionBar.addTab(base,command=lambda n=l: displayLog(n))
		#Store
		loadedLogs[counter]=l

def refreshLogs():
	"""
	Will refresh the logs
	this works by getting the current index
	of the selection bar. When each log is added
	it is stored with an index and these indexes
	are used to indentify the logs
	"""
	#Get the current log being viewed
	currentLog=logSelectionBar.currentIndex
	if currentLog in loadedLogs:
		displayLog(loadedLogs[currentLog])


def displayLog(logDirectory):
	"""
	Function to load a log to the
	screen
	"""
	#Open the log file
	try:
		file=open(logDirectory,"r")
	except:
		log.report("Error opening log file")
	else:
		content=file.readlines()
		file.close()
		#Clear the tree
		logTree.delete(*logTree.get_children())
		#Get data
		for line in content:
			sections=line.split(",")
			tag=""
			try:
				tag=sections[2]
			except:
				log.report("Log index error getting tag",tag="Error")
			logTree.insertData(sections,tag)
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
	#Clear listbox
	openListbox.secureClear()
	if len(files) > 0:
		#Iterate
		for file in files:
			#Get master pod name
			displayName=getRootName(file)
			#Create instance
			masterPodInstance=loadMasterPodFromFile(file)
			#First check if the master pod is valid
			if masterPodInstance:
				addMasterPodToScreen(masterPodInstance)
			else:
				log.report("Invalid Master Pod found",tag="Important")

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
		checkTimeRemaining(currentSelection)
	else:
		showMessage("Select Pod","Please select a master pod")

def initiateNewMasterPod(**kwargs):
	"""
	Function called when user clicks
	the button to create a new master pod
	"""
	masterPodName=kwargs.get("Master Pod Name",None)
	masterPodPassword=kwargs.get("Password",None)
	masterPodHint=kwargs.get("Hint",None)
	if masterPodName and masterPodPassword:
		newMasterPod=masterPod(masterPodName)
		#Add the hint
		if masterPodHint:
			newMasterPod.hint=masterPodHint
		newMasterPod.addKey(masterPodPassword)
		newMasterPod.save()
		#Add to screen
		addMasterPodToScreen(newMasterPod)
		#Report to log
		log.report("Created a new masterPod",masterPodName)

def createNewMasterPodWindow():
	"""
	Launches a new data window
	to allow user to create a new
	master pod
	"""
	newWindow=dataWindow(window,"Create Master Pod")
	newWindow.functionToRun=initiateNewMasterPod
	#Add the sections
	masterPodNameSection=dataSection(newWindow.contentArea,advancedEntry,"Master Pod Name",cannotContain=masterPod.loadedPods.keys())
	masterPodNameSection.pack()
	masterPodPassword=dataSection(newWindow.contentArea,advancedEntry,"Password",hide=True)
	masterPodPassword.pack()
	masterPodConfirm=dataSection(newWindow.contentArea,advancedEntry,"Confirm",mustBeSameAs=masterPodPassword,hide=True)
	masterPodConfirm.pack()
	masterHint=dataSection(newWindow.contentArea,advancedEntry,"Hint",checkNeeded=False)
	masterHint.pack()
	masterHint.dataValid=True
	masterHint.changeColour=False

	#Add to window
	newWindow.addDataSection(masterPodNameSection)
	newWindow.addDataSection(masterPodPassword)
	newWindow.addDataSection(masterPodConfirm)
	newWindow.addDataSection(masterHint)

def openExternalMasterPod(importOrMove):
	"""
	Launch a dialog to allow
	user to move a master pod locally

	ImportOrMove = "Import" = Edit in own directory
	ImportOrMove = "Move" = move the file locally then edit
	"""
	directory=askForFile(("Master Pod",".mp"))
	#If user did not cancel
	if directory:
		baseName=getRootName(directory)
		if baseName in masterPod.loadedPods:
			showMessage("Loaded","This master pod has been loaded")
		else:

			if importOrMove == "Move":
				"""
				If the master pod should be moved 
				to a local directory for future use
				"""
				#Move locally
				newDirectory=getCertainDirectory("Data")
				moveFile(directory,newDirectory)
				#Re scan
				findMasterPods(getWorkingDirectory())

			else:
				"""
				If the master pod should be opened
				and saved externally
				"""
				masterPodInstance=loadMasterPodFromFile(directory)
				if masterPodInstance:
					#Update the location
					masterPodInstance.location=directory
					#Add to listbox
					addMasterPodToScreen(masterPodInstance)
				else:
					log.report("Not a valid master pod loaded",tag="Important")
					showMessage("Error","This is not a valid Master Pod")

			#Show the correct screen
			openScreen.show()
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

def runCountdown(lockedValue,masterPodInstance):
	"""
	Will run the countdown timer on the login
	screen 
	"""
	currentTime=getCurrentTime()
	while lockedValue > currentTime:
		currentTime=getCurrentTime()
		if lockedValue > currentTime:
			timeRemaining=calculateTimeRemaining(lockedValue,currentTime,"string")
			loginAttemptVar.set(masterPodInstance.masterName+" pod has been locked\nTime remaining: "+timeRemaining)
		else:
			checkTimeRemaining(masterPodInstance)
			loginAttemptVar.set(masterPodInstance.masterName+" pod has been unlocked")
		time.sleep(0.2)

def checkTimeRemaining(masterPodInstance,**kwargs):
	"""
	Function that is called
	to check if the current master
	pod is still locked. If so
	change the screen. It is also
	used to change screen if user
	failed attempt
	False = Pod not locked
	True = Pod is locked
	
	resetScreen: False = failed attempt
	resetScreen: None = do nothing
	showLocked: True = show messagebox
	"""
	#Kwargs that can be specified
	resetScreen=None
	resetScreen=kwargs.get("resetScreen",resetScreen)
	showLocked=None
	showLocked=kwargs.get("showLocked",showLocked)
	#Check is valid type
	if type(masterPodInstance) is masterPod:
		if hasattr(masterPodInstance,"locked"):
			#Get the value in the pod and the current time
			lockedValue=masterPodInstance.locked
			if lockedValue is not None:
				currentTime=getCurrentTime()
				if lockedValue > currentTime:
					#Calculate time remaining
					timeRemaining=calculateTimeRemaining(lockedValue,currentTime,"string")
					mainThreadController.runThread("runCountdown",lockedValue=lockedValue,masterPodInstance=masterPodInstance)
					loginScreen.colour(mainLockedColour)
					#Show messagebox if specified
					if showLocked:
						showMessage("Locked","This master pod is locked")
					return True

				elif resetScreen == False:

					#Attempt to get number of attempts from dict
					if masterPodInstance in masterPodAttempts:
						loginAttemptNumberVar.set(masterPodAttempts[masterPodInstance])
					#If not just add one
					else:
						loginAttemptNumberVar.set(loginAttemptNumberVar.get()+1)

					#The password was incorrect
					loginAttemptVar.set("Incorrect Password "+"("+str(loginAttemptNumberVar.get())+")")
					#Colour the screen incorrect colour
					loginScreen.colour(mainRedColour)
					return False

				elif lockedValue < currentTime:
					#Reset the screen
					loginScreen.colour(mainFrame.windowColour)

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
		unlockAttempt=checkMasterPodAttempt(masterPod.currentMasterPod, attempt)
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
			checkTimeRemaining(masterPod.currentMasterPod,resetScreen=False,showLocked=True)
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
		podListbox.addObject(podInstance.peaName,podInstance,colour=podColour)

	#Clear the search so it resets when loading screen
	resetSearch(podSearchEntry,runSearch)

def openPod(podObject):
	"""
	This function is run
	when user double clicks
	on a pod in the listbox
	"""
	selectedPod=podObject
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
	if masterPod.currentMasterPod:
		#Save
		masterPod.currentMasterPod.save()
		#Remove the key from box
		del keyBox.keyHoles[masterPod.currentMasterPod]
	#Show the correct frame
	openScreen.show()

def initiateNewPeaPod(**kwargs):
	"""
	Initiate a new peaPod
	given the correct parameters
	"""
	podName=kwargs.get("Pod Name",None)
	template=kwargs.get("Template",None)
	if podName and template:
		#Create the pea
		newPeaPod=masterPod.currentMasterPod.addPeaPod(podName,template=template)
		#Add to listbox
		podListbox.addObject(podName,newPeaPod)
		#Refresh the listbox
		loadPodsToScreen()
		#Save
		masterPod.currentMasterPod.save()
		#Report to log
		log.report("Created a new pea pod for",masterPod.currentMasterPod.masterName)

def createNewPeaPodWindow(**kwargs):
	"""
	Function to launch the window
	to allow the user to enter
	name and details for a new peaPod
	"""
	global currentPeaWindow
	newWindow=dataWindow(window,"Create Pea Pod")
	#Update the global variable
	currentPeaWindow=newWindow
	newWindow.functionToRun=initiateNewPeaPod
	#Create Section
	allPodNames=masterPod.currentMasterPod.peas.keys()
	podName=dataSection(newWindow.contentArea,advancedEntry,"Pod Name",cannotContain=allPodNames)
	podName.pack()
	templateOption=dataSection(newWindow.contentArea,advancedOptionMenu,"Template",
							   values=podTemplate.templates.keys(),default="Login",
							   optionCommand=changePopupColour)
	templateOption.pack()

	#Add the sections
	newWindow.addDataSection(podName)
	newWindow.addDataSection(templateOption)
	#Ititate colour
	changePopupColour("Login")

def runSearch():
	"""
	This function is called when the user
	types into the search bar
	"""
	global processLanguageOn
	dataToFind=getDataFromWidget(podSearchEntry)
	#Search through the keys otherwise data changes
	dataSource=podListbox.data.keys()
	#Store the results of the search
	results=[]
	#Search the data source
	for item in dataSource:
		if searchDataSource(dataToFind,[item],capital=True,full=False):
			results.append(item)

	#Add the results to screen
	podListbox.delete(0,END)
	for item in results:
		podListbox.addExisting(item)

	if processLanguageOn:
		processSearchLanguage(podSearchEntry)

def showKey():
	"""
	Function will show
	the user a key explaining
	the pods
	"""
	newWindow=topWindow(window)
	#Config Context Bar
	newWindow.context.removePlaceholder(0)
	#Context commands
	newWindow.context.updateContextButton(0,command=lambda n=newWindow: n.grab_release())
	newWindow.context.updateContextButton(1,command=lambda n=newWindow: n.destroy())
	#Add Table
	newTable=table(newWindow,"Pod Templates",False)
	newTable.pack(fill=BOTH,expand=True)
	#Add the content to the table
	for t in podTemplate.templateColours:
		rowName=t+" colour:"
		rowColour=podTemplate.templateColours[t]
		newTable.addRow(rowName,t,rowColour)

	newWindow.run()

#======View Pod Screen========

def deletePod(peaPodInstance,**kwargs):
	"""
	Will delete peaPod
	from a masterPod class
	"""
	returnToHome=True
	returnToHome=kwargs.get("returnToHome",returnToHome)

	choice=messagebox.askokcancel("Sure","Are you sure you want to delete this pod?")
	if choice:
		currentMaster=masterPod.currentMasterPod
		for pea in currentMaster.peas:
			currentPeaPod=currentMaster.peas[pea]
			if currentPeaPod == peaPodInstance:
				del currentMaster.peas[pea]
				break
		#Save
		currentMaster.save()

		if returnToHome:
			goHome()

#======Generate Screen========

def genPassword(charOrWords):
	"""
	The function called when
	a password needs to be generated 
	"""
	currentGenPasswordMethod.set(charOrWords)
	if charOrWords == "words":
		#Get the data from sliders etc
		numberOfWords=genPasswordWordsLengthSlider.getValue()
		seperator=genPasswordWordsSeperatorVar.get()
		commonWords=genPasswordWordCommonVar.get()
		password=generateWordPassword(numberOfWords,seperator,genPasswordWordCommonVar.get())
	else:
		#Get the length and amount of symbols etc
		numberOfCharacters=genPasswordCharLengthSlider.getValue()
		numberOfDigits=genPasswordDigitsSlider.getValue()
		numberOfSymbols=genPasswordSymbolsSlider.getValue()
		#Generate the password
		password=generatePassword(numberOfCharacters,numberOfSymbols,numberOfDigits)
	genPasswordVar.set(password)

	#Calculate password strength
	passwordStrength=calculatePasswordStrength(password,split=genPasswordWordsSeperatorVar.get())
	passwordWeight=passwordStrength[4]
	passwordScoreString=passwordStrength[5]
	#Show labels
	if passwordScoreString == "Strong":
		genPasswordStrengthVar.set("Strong password")
		genPasswordLabel.config(fg="#66BC15")

	elif passwordScoreString == "Medium":
		genPasswordStrengthVar.set("Medium password")
		genPasswordLabel.config(fg=mainOrangeColour)

	else:
		genPasswordStrengthVar.set("Weak password")
		genPasswordLabel.config(fg=mainRedColour)

	#Add to the review screen
	addDataToWidget(genReviewEntry,password)
	reviewPassword()

def reviewPassword():
	"""
	The function to 
	review a password
	and tell the user
	how to improve
	the password
	
	"""
	#Collect data
	passwordData=genReviewEntry.get()

	strength=calculatePasswordStrength(passwordData)
	results=strength[3]
	#Clear tree
	genReviewTree.delete(*genReviewTree.get_children())
	#Add the data to the tree
	"""
	False = Passed Test
	True = Failed Test
	"""
	#Iterate through the Tree
	for item in results:
		#Get the result in the dictionary
		value=results[item]
		#If the value is true the test failed
		if value:
			tag="Fail"
			message="Incomplete"
		#Test passed
		else:
			tag="Pass"
			message="Complete"
		#Add data to tree
		genReviewTree.insertData((item, message), tag)

def launchPasswordToPodPopup():
	"""
	Launches a popup window
	to allow user to select pod
	to add password to
	"""

	#Get list of pods with password fields
	allPeaPods=masterPod.currentMasterPod.peas
	filter=[]
	for item in allPeaPods:
		peaObject=allPeaPods[item]
		peaTemplate=peaObject.templateType
		peaTemplate=podTemplate.templates[peaTemplate]
		if peaTemplate.containsPassword:
			filter.append(item)

	if len(filter) > 0:
		newWindow=dataWindow(window,"Select Pod")

		#Remove the clear button
		newWindow.context.hideButton(1)
		#Change button name
		newWindow.context.updateContextButton(2,text="Update")

		#Create option menu
		podOption=dataSection(newWindow.contentArea,advancedOptionMenu,"Select Pod",values=filter,optionCommand=lambda event:newWindow.checkAll())
		podOption.pack()
		newWindow.addDataSection(podOption)
		newWindow.functionToRun=addPasswordToPod
	else:
		showMessage("No Password","No Pods found to add password to")

def addPasswordToPod(**kwargs):
	"""
	Function that will take the password
	that has been generated and add it
	to the selected pod
	"""
	chosenPod=kwargs.get("Select Pod",None)
	if chosenPod:
		#Get the correct pod
		allPeaPods=masterPod.currentMasterPod.peas
		if chosenPod in allPeaPods:
			currentPeaPod=allPeaPods[chosenPod]
			if currentPeaPod.vaultState:
				currentPeaPod.unlockVault("Unlock")

			#Get password
			password=None
			if currentReviewOrGen.get() == "Review":
				password=getDataFromWidget(genReviewEntry)
			elif currentReviewOrGen.get() == "Generate":
				password=genPasswordVar.get()
			#Update password
			if password:
				currentPeaPod.vault["Password"]=password
			#Show the screen
			openPod(currentPeaPod)
			#Save
			masterPod.currentMasterPod.save()

def changeGenerateType(indicator):
	"""
	Function is called when user
	switches from generate to review
	to know what data to copy to clipboard
	"""
	global currentReviewOrGen
	if indicator == "Review":
		context.updateContextButton(0,command=lambda:copyToClipboard(getDataFromWidget(genReviewEntry)))
		currentReviewOrGen.set("Review")
	else:
		context.updateContextButton(0,command=lambda:copyToClipboard(genPasswordVar.get()))
		currentReviewOrGen.set("Generate")

def toggleGenerateEntry():
	"""
	Function to hide and show
	the contents of the review
	password entry
	"""
	if genHideEntryVar.get() == True:
		genReviewEntry.config(show="•")
		genReviewEntryToggleHide.config(text="Show")
	else:
		genReviewEntry.config(show="")
		genReviewEntryToggleHide.config(text="Hide")

def loadReview():
	"""
	Function to load review password
	when clicked in the menu
	"""
	genPasswordScreen.show()
	genPasswordNotebook.selectionBar.runTabCommand(1)

#======Password Screen========

def addCommonPasswordToListbox(dataList):
	dataList=sorted(dataList)
	counter=0
	passwordDataListbox.delete(0,END)
	for word in dataList:
		counter+=1
		if counter % 2 == 0:
			passwordDataListbox.addObject(word,word,colour="#FFFFFF")
		else:
			passwordDataListbox.addObject(word,word,colour="#EAE9EB")

def searchCommonPasswords():
	"""
	Search the common passwords
	"""
	global threadRunning
	userRequest=passwordSearchEntry.getData()
	if userRequest is None:
		userRequest=""


	dataSource=passwordDataListbox.data.keys()
	results=[]
	for item in dataSource:
		if searchDataSource(userRequest,[item],capital=True,full=False):
			results.append(item)

	#Add to listbox
	addCommonPasswordToListbox(results)


#======Audit Screen========

def displayAudit():
	"""
	Will dislpay the results from an audit
	"""
	auditResults=runAudit(masterPod.currentMasterPod)
	#Get results and duplicates
	allResults=auditResults["ResultDict"]
	duplicateResults=auditResults["DuplicateDict"]

	#Display score
	auditScore=auditResults["Overall"]
	auditScoreVar.set(str(auditScore)+"%")

	if auditScore >= 60:
		auditScoreLabel.update(fg=mainGreenColour)
	elif auditScore >= 45:
		auditScoreLabel.update(fg=mainOrangeColour)
	else:
		auditScoreLabel.update(fg=mainRedColour)

	#Go through the results
	for itemName in auditTable.rowInfo:
		if itemName in auditResults:
			#Update the label
			auditTable.updateRow(itemName,auditResults[itemName])


	#Update the buttons to they update on clicks
	for rowText in auditTable.buttonInfo:
		if rowText == "All accounts":
			auditTable.updateButtonCommand(rowText,lambda: showAuditResults(allResults))
		elif rowText == "Strong Passwords":
			sendResults={}
			filterResults=[k for k,v in allResults.items() if v == 'Strong']
			for i in filterResults:
				sendResults[i]=allResults[i]
			auditTable.updateButtonCommand(rowText,lambda s=sendResults: showAuditResults(s))

		elif rowText == "Average Passwords":
			sendResults={}
			filterResults=[k for k,v in allResults.items() if v == 'Medium']
			for i in filterResults:
				sendResults[i]=allResults[i]
			auditTable.updateButtonCommand(rowText,lambda s=sendResults : showAuditResults(s))

		elif rowText == "Weak Passwords":
			sendResults={}
			filterResults=[k for k,v in allResults.items() if v == 'Weak']
			for i in filterResults:
				sendResults[i]=allResults[i]
			auditTable.updateButtonCommand(rowText,lambda s=sendResults: showAuditResults(s))

		elif rowText == "Duplicates":
			auditTable.updateButtonCommand(rowText,lambda: showAuditResults(duplicateResults))

	#Clear the tree
	auditResultsTree.delete(*auditResultsTree.get_children())

def showAuditResults(resultsDict):
	"""
	This function will show the results 
	from the audit. The parameter is 
	a dict. key = podName value = stength
	"""
	#Clear the tree
	auditResultsTree.delete(*auditResultsTree.get_children())
	#Add the results
	for item in resultsDict:
		strength=resultsDict[item]
		auditResultsTree.insertData((item.peaName,strength),[strength])


#======Other functions========

def filterPodListbox(templateType):
	"""
	Will filter the contents of
	the pod listbox to contain
	only one kind of template type
	"""

	#Check the name is valid first
	found=False
	templateType=templateType.upper()
	for template in podTemplate.templates:
		if template.upper() == templateType:
			found=True

	#if the template type is valid then find matching pods
	if found:
		peas=findPeasWithTemplate(templateType)
		if len(peas) > 0:
			for pea in peas:
				if type(pea) is peaPod:
					podListbox.addExisting(pea.peaName)
				elif type(pea) is str:
					podListbox.addExisting(pea)

def findPeasWithTemplate(templateType):
	"""
	Function to find peas with a certain
	template name
	"""
	templateType=templateType.upper()
	results=[]
	#Search through the currently loaded master pod
	for peaName in masterPod.currentMasterPod.peas:
		peaObject=masterPod.currentMasterPod.peas[peaName]
		#If the attribute matches then add to results
		if peaObject.templateType.upper() == templateType:
			results.append(peaObject)
	return results

def orderPodListbox(orderMethod):
	"""
	Will order the data inside
	the pod listbox
	"""
	validOrderMethods=["NAME","TYPE"]
	orderMethod=str(orderMethod).upper()
	newList=[]
	#Add the current data dictionary into list for sorting
	for item in podListbox.data.keys():
		newList.append(item)

	#Check the order method is valid
	if orderMethod in validOrderMethods:
		if orderMethod == "NAME":
			newList=orderList(newList)

		elif orderMethod == "TYPE":
			print("Can not sort by type yet")

		#Add the original data
		podListbox.delete(0,END)
		for item in newList:
			podListbox.addExisting(item)

def orderList(dataSource,**kwargs):
	"""
	Will order a list in a certain way
	"""
	return sorted(dataSource)

def resetSearch(entry,searchCommand):
	"""
	Will clear an entry
	and run a search command
	to reseet search 
	"""
	addDataToWidget(entry,"")
	runCommand(searchCommand)

def changePopupColour(templateVar):
	"""
	Function will change the colour
	of the popup window when the user selects
	a template
	"""
	global currentPeaWindow
	if templateVar in podTemplate.templateColours and currentPeaWindow:
		correctColour=podTemplate.templateColours[templateVar]
		currentPeaWindow.sectionData["Template"].label.config(fg=correctColour)
		#currentPeaWindow.status.colour(correctColour)


#====================Thread commands====================
mainThreadController.createThread("runCountdown",runCountdown)

#====================Button commands====================

#Splash Screen
splashScreen.updateCommand(0,command=lambda: logScreen.show())
splashScreen.updateCommand(1,command=lambda: openScreen.show())
splashScreen.updateCommand(2,command=lambda: closeProgram())
#Log screen
logScreen.updateCommand(0,command=lambda: refreshLogs())
logScreen.updateCommand(1,command=lambda: goHome())
#Open Screen
openScreen.updateCommand(0,command=lambda: createNewMasterPodWindow())
openScreen.updateCommand(1,command=lambda: loadMasterPodToLogin())
#Login Screen
loginScreen.updateCommand(2,command=lambda: openScreen.show())
loginScreen.updateCommand(0,command=lambda: showHint())
loginScreen.updateCommand(1,command=lambda: attemptMasterPodUnlock())
#Pod screen
podScreen.updateCommand(0, command=createNewPeaPodWindow)
podScreen.updateCommand(2,command=lambda: exitPod())
podScreen.updateCommand(1,command=lambda: openPod(podListbox.getSelection()))
#View Pod screen
viewPodScreen.updateCommand(2,command=lambda: podScreen.show())
viewPodScreen.updateCommand(1,command=lambda: viewPodNotebook.startEdit())
viewPodScreen.updateCommand(0,command=lambda: deletePod(masterPod.currentMasterPod.currentPeaPod))
#Generate screen
genPasswordScreen.updateCommand(1,command=lambda: genPassword(currentGenPasswordMethod.get()))
genPasswordScreen.updateCommand(2,command=lambda: launchPasswordToPodPopup())
genPasswordScreen.updateCommand(0,command=lambda: copyToClipboard(genPasswordVar.get()))
genPasswordScreen.updateCommand(3,command=lambda: goHome())
#Password screen
passwordScreen.updateCommand(1,command=lambda: goHome())
#Audit screen
auditScreen.updateCommand(0,command=lambda: goHome())
#====================Screen commands====================
#Login Screen
loginScreen.addScreenCommand(lambda: loginAttemptNumberVar.set(0))
loginScreen.addScreenCommand(lambda: loginEntry.resetEntry())
loginScreen.addScreenCommand(lambda: loginScreen.colour(mainFrame.windowColour))
loginScreen.addScreenCommand(lambda: loginAttemptVar.set(""))
loginScreen.addScreenCommand(lambda: loginFileVar.set(masterPod.currentMasterPod.masterName))
#Pod Screen
podScreen.addScreenCommand(lambda: loadPodsToScreen())
#Generate screen
genPasswordNotebook.addScreenCommand("Generate",lambda:changeGenerateType("Generate") )
genPasswordNotebook.addScreenCommand("Review",lambda:changeGenerateType("Review") )
#Audit screen
auditScreen.addScreenCommand(lambda: displayAudit())
#====================Context====================
#Pod Screen
podSearchContext.updateContextButton(0,text="Sort by name",enabledColour="#EBF2F2",command=lambda: orderPodListbox("Name"))
podSearchContext.updateContextButton(1,text="Reset",command=lambda: resetSearch(podSearchEntry,runSearch),enabledColour="#DCE9E7")
podContext.updateContextButton(0,command=lambda: genPasswordScreen.show())
podContext.updateContextButton(1,command=lambda: loadReview())
podContext.updateContextButton(2,command=lambda: auditScreen.show())
podContext.updateContextButton(3,command=showKey)

#Password screen
passwordScreenTopContext.updateContextButton(0,command=lambda: resetSearch(passwordSearchEntry,searchCommonPasswords))
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
recursiveBind(podListbox,"<Double-Button-1>",lambda event: openPod(podListbox.getSelection()))
recursiveBind(podSearchEntry,"<KeyRelease>",lambda event: runSearch())
#Generate password
genReviewEntry.bind("<KeyRelease>",lambda event: reviewPassword())
genPasswordLabel.bind("<Double-Button-1>",lambda event: genPasswordLabel.expandText("Password"))
#Password screen
passwordSearchEntry.bind("<KeyRelease>",lambda event: searchCommonPasswords())

#====================Slider commands====================
genPasswordCharLengthSlider.addCommand(lambda:genPassword("char"))
genPasswordDigitsSlider.addCommand(lambda: genPassword("char"))
genPasswordSymbolsSlider.addCommand(lambda: genPassword("char"))
genPasswordWordsLengthSlider.addCommand(lambda: genPassword("words"))
#====================Checkbutton commands====================

genReviewEntryToggleHide.config(command=toggleGenerateEntry)

#====================MENUS===================


#----Private Menus----
#Add cascades
privateMenu.add_cascade(label="File",menu=privateFileMenu)
privateMenu.add_cascade(label="Password",menu=privatePasswordMenu)

#File
privateFileMenu.add_command(label="Show threads",command=lambda: print(mainThreadController))
#Password
privatePasswordMenu.add_command(label="Generate Password",command=lambda: genPasswordScreen.show())
privatePasswordMenu.add_command(label="Review Password",command=loadReview)
privatePasswordMenu.add_command(label="View common passwords",command=lambda: passwordScreen.show())
privatePasswordMenu.add_command(label="Security Audit",command=lambda: auditScreen.show())

#----Public menu----
#Add cascades
publicMenu.add_cascade(label="File",menu=publicFileMenu)

#File
publicFileMenu.add_command(label="Move Master Pod Locally", command=lambda: openExternalMasterPod("Move"))
publicFileMenu.add_command(label="Open External Master Pod", command=lambda: openExternalMasterPod("Import"))

#====================Testing Area====================

#====================Initial Loaders====================

#Find the current master pods
runCommand(lambda: findMasterPods(getWorkingDirectory()),name="Finding master pods")
#Generate a password initially on screen
genPassword("char")
changeGenerateType("Generate")
#Load the common passwords to the program
addCommonPasswordToListbox(commonPasswords)
#Load the log files
showAllLogs()

#Last call
runCommand(lambda: splashScreen.show(),name="Splash loader")
#====================END====================

window.mainloop()

