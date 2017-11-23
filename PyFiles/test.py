
#====================Imports====================
from tkinter import *
from PyUi import *
from PEM import *

#====================PyPassword Window Class====================

class PyPasswordWindow(Tk):
	"""
	This is the window class where
	the main PyPassword program is created
	"""
	def __init__(self):
		Tk.__init__(self)

		#=====Window Setup=====

		self.title("PyPassword 3")
		self.geometry("570x450")

		#=====Status/Context=====

		#Status variables
		self.statusVar=StringVar()
		self.statusVar.set("Home")
		#Set screen variable up
		screen.statusVar=self.statusVar
		#Create the label for status
		self.statusBar=mainLabel(self,textvariable=self.statusVar,font="Avenir_Bold 15")
		#Display the bar
		self.statusBar.colour("#24544C")
		self.statusBar.pack(side=BOTTOM,fill=X)

		#Initiate the context bar for the whole program
		self.context=contextBar(self)
		self.context.pack(side=BOTTOM,fill=X)

		#=====Splash screen=====

		#Create screen using screen class
		self.splashScreen=screen(self,"PyPassword")
		#Setup Context bar
		self.splashScreen.context=self.context

		#Go to pods
		self.splashScreen.addContextInfo(0,text="View Log",enabledColour="#17F388",
									hoverColour="#13C770",clickedColour="#41F59D")
		#View Log
		self.splashScreen.addContextInfo(1,text="Go to pods",enabledColour="#A5F413",
									hoverColour="#7CCE32",clickedColour="#B5F426")
		#Exit
		self.splashScreen.addContextInfo(2,text="Exit",enabledColour="#FFA500",
									hoverColour="#E89600",clickedColour="#FFB52E")

		#Create centered frame for logo
		self.splashCenter=mainFrame(self.splashScreen)
		self.splashCenter.pack(expand=True)

		#Get the logo for PyPassword and create image label
		try:
			self.splashImage=getPicture("PyPassword 3 logo.gif")
			self.splashLabel=Label(self.splashCenter,image=self.splashImage)
			self.splashLabel.pack()
		except:
			pass

		#Create the title
		self.splashTitle=mainLabel(self.splashCenter,text="PyPassword",font="Avenir 39",fg="#43D4A0")
		self.splashTitle.pack()


		#=====Open screen=====

		self.openScreen=screen(self,"Open")
		self.openScreen.colour("#ADDCFC")

		#Top label
		self.openTopLabel=topLabel(self.openScreen,text="Select Master Pod")
		self.openTopLabel.pack(side=TOP,fill=X)

		#Context
		self.openScreen.context=self.context
		self.openScreen.addContextInfo(0,text="Create New")
		self.openScreen.addContextInfo(1,text="Open",enabledColour="#2EE697")
		self.openScreen.addContextInfo(2,text="Open Other")

		#Listbox
		self.openListbox=advancedListbox(self.openScreen,font="Avenir 37")
		self.openListbox.pack(expand=True,fill=BOTH)


		#=====Button commands=====
		self.splashScreen.updateCommand(1,command=lambda: self.openScreen.show())
		self.openScreen.updateCommand(0,command=self.createNew)

		#=====Initial Run=====

		#Find the master pods
		self.loadMasterPods(getWorkingDirectory())
		#Show the splash screen
		self.splashScreen.show()

	def createNew(self):
		new=PyPasswordWindow()

	def loadMasterPods(self,directory):
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
				self.addMasterPodToScreen(masterPodInstance)

		else:
			log.report("No mp files found in directory")
			return None

	def addMasterPodToScreen(self,masterPodInstance):
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
			self.openListbox.addObject(displayName,masterPodInstance,colour=masterPodColour)
			#Add to dictionary
			masterPod.loadedPods[displayName]=masterPodInstance

newWindow=PyPasswordWindow()
newWindow.mainloop()

second=PyPasswordWindow()
second.mainloop()


