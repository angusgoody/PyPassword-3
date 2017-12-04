# coding=utf-8

#Angus Goody
#12/10/17
#PyPassword 3 User Interface Module

"""
This file is the user interface module
and is where all the user interface elements 
are created and used.
"""

#====================Imports====================
from tkinter import *
from PEM import *
from random import randint
#====================Log====================

log=logClass("User Interface")
log.saveLog()
#====================Preset variables====================
incorrectColour="#E4747D"
correctColour="#64D999"

def test():
	print("test function")
#====================Functions====================
"""
This section is for functions that aid with the user
interface elements of PyPassword
"""
#Utility functions

def runCommand(command,**kwargs):
	"""
	This function will safeley run
	a command and handle any errors
	and report to log while returning
	results
	"""
	#Collect idetifier from KWARGS
	identifier="No Data Available"
	identifier=kwargs.get("name",identifier)
	#Run the command
	try:
		content=command()
	except Exception as e:
		print("Error running command",identifier,e,command)
		log.report("Error executing command through function",command,tag="Error")
	else:
		log.report("Command executing success",identifier,tag="System")
		return content

def showMessage(pre,message):
	"""
	Function to show a tkinter
	message using messagebox
	"""
	try:
		messagebox.showinfo(pre,message)
	except:
		print(message)

def insertEntry(entry,message):
	"""
	This function is used
	for adding data to widgets 
	"""
	entry.delete(0,END)
	entry.insert(END,message)

#Recursion
def recursiveBind(parent,bindButton,bindFunction,**kwargs):
	"""
	This function will bind a function
	recursively to a widget, this means
	all the children of the widget
	will also be binded to the same function
	"""
	#Check if the parent has children
	if "winfo_children" in dir(parent):
		#Bind the parent
		parent.bind(bindButton,bindFunction)
		#Bind the children
		for child in parent.winfo_children():
			recursiveBind(child,bindButton,bindFunction)
	else:
		try:
			parent.bind(bindButton,bindFunction)
		except:
			log.report("Could not bind function to",type(parent))

def basicChangeColour(widget,colour):
	#Items who's highlight background is changed
	highlightItems=["Entry", "Button", "Text", "Listbox", "OptionMenu", "Menu"]
	#Change colour
	if type(widget) in highlightItems:
		widget.config(highlightbackground=colour)
	else:
		widget.config(bg=colour)

def recursiveColour(parent, colour, **kwargs):
	"""
	The recursive colour function
	will change the colour of widgets
	recursively
	"""
	#Items to exclude
	excludeItems=[Entry,advancedEntry]

	#Check to see if any widgets should be excluded
	if "exclude" in kwargs:
		#Add new items to exclude
		excludeItems.extend(kwargs["exclude"])

	overide=False
	if "overide" in kwargs:
		overide=kwargs["overide"]
	#Check parent is valid
	if type(parent) not in excludeItems:

		#Get parent attributes and methods
		parentAtt=dir(parent)

		#Check other attributes
		valid=True
		if "preserveColour" in parentAtt:
			if parent.preserveColour:
				valid=False
		if overide:
			valid=True
		if valid:
			#Change parent
			basicChangeColour(parent,colour)
			#Check for children
			if "winfo_children" in parentAtt:
				for child in parent.winfo_children():
					recursiveColour(child,colour,exclude=excludeItems,overide=overide)

#Hex
def convertHex(value,intoDecOrHex):
	"""
	Convert a decimal to hex or hex to decimal
	"""
	if intoDecOrHex == "Decimal":
		return int("0x" + str(value), 16)
	else:
		hexValue = "#"
		hexValue = hexValue + str((format(value, '02x')).upper())
		return hexValue

def getHexSections(hexValue):
	"""
	This will split a 6 digit hex number into pairs and store them
	in an array
	"""
	if len(hexValue) <= 7 and "#" in hexValue:
		#Removes the #
		colourData = hexValue.replace("#", "")
		# Split HEX number into pairs
		colourSections = [colourData[i:i + 2] for i in range(0, len(colourData), 2)]
		return colourSections

def getDecimalHexSections(hexValue):
	hexSections=getHexSections(hexValue)
	decimalArray=[]
	for item in hexSections:
		decimalValue=convertHex(item,"Decimal")
		decimalArray.append(decimalValue)
	return decimalArray

def getColourForBackground(hexValue):
	"""
	This function will return white or black as a text colour
	depending on what the background colour passed to it is. For
	example if a dark background is passed then white will be returned because
	white shows up on dark best.
	"""
	chosenColour="Black"
	whiteCounter = 0

	#Checks the hex number is standard
	if len(hexValue) <= 7 and "#" in hexValue:

		colourSections=getHexSections(hexValue)
		for x in colourSections:
			#Convert to decimal
			y=convertHex(x,"Decimal")
			#If its less than half way between 0 and FF which is 255
			if y < 128:
				whiteCounter += 1
		if whiteCounter > 1:
			#White is returned
			chosenColour = "#ffffff"
		else:
			#Black is returned
			chosenColour = "#000000"
	return chosenColour

def generateHexColour():
	"""
	This function will generate a random HEX colour

	"""
	baseNumber=randint(1,16777216)
	hexValue=convertHex(baseNumber,"Hex")
	hexLeng=len(hexValue)
	while hexLeng != 7:
		hexValue=hexValue+"0"
		hexLeng=len(hexValue)
	return hexValue

#====================Core Classes====================
"""
Core Classes are the core custom classes in PyPassword
that are the top level of objects.
"""

class mainFrame(Frame):
	"""
	The mainFrame is the core
	class of PyPassword and makes
	up most of the user interface elements
	in PyPassword. It is a frame class
	which has more customization and efficiency.
	"""
	def __init__(self,parent,**kwargs):
		Frame.__init__(self,parent)

		#Should colour be changed during recursion
		self.preserveColour=False
		#Store the default window colour
		self.windowColour="#FFFFFF"

	def colour(self,chosenColour,**kwargs):
		"""
		The colour method will change 
		the colour of the frame and all
		the children of the frame 
		"""
		recursiveColour(self,chosenColour,**kwargs)

	def addBinding(self,bindButton,bindFunction,**kwargs):
		"""
		This method will allow the widget
		to be binded to a function recursively meaning
		all the children are also binded.
		"""
		recursiveBind(self,bindButton,bindFunction,**kwargs)

class mainButton(mainFrame):
	"""
	The main Button class
	if a custom button class
	that handles bindings and colours
	etc
	"""
	def __init__(self,parent,**kwargs):
		mainFrame.__init__(self,parent)
		#Preserve button colour
		self.preserveColour=True
		#Store the command
		self.command=None
		#Store button state
		self.state=True
		self.hoverOn=False
		self.pressing=False
		#Fonts
		self.font="Avenir 14"
		#Button colour variables
		self.enabledColour="#FFFFFF"
		self.enabledFG="#000000"
		self.hoverColour="#F4F3F5"
		self.clickedColour="#A9F955"
		self.disabledColour="#ACB4B4"
		self.disabledFG="#939797"
		#Width
		self.labelWidth=12
		#Text
		self.textVar=StringVar()
		self.textVar.set("Button")
		self.textLabel=mainLabel(self,textvariable=self.textVar,width=self.labelWidth,font=self.font)
		self.textLabel.pack(expand=True)
		#Bindings
		self.addBinding("<Enter>",lambda event: self.hover(True))
		self.addBinding("<Leave>",lambda event: self.hover(False))
		self.addBinding("<Button-1>",lambda event: self.runCommand())
		self.addBinding("<ButtonRelease-1>",lambda event: self.pressBind(False))

		#Check for Kwargs
		self.updateButton(**kwargs)

		#Initiate Button state
		#self.changeState(True)

	def updateButton(self,**kwargs):
		"""
		This method will allow all aspects
		of the button to be updated using
		kwargs
		"""
		#Get kwargs
		self.font=kwargs.get("font",self.font)
		self.textVar.set(kwargs.get("text",self.textVar.get()))
		self.textVar=kwargs.get("textvariable",self.textVar)
		self.command=kwargs.get("command",self.command)
		self.textLabel.config(width=kwargs.get("width",self.labelWidth))
		#Colour kwargs
		self.enabledColour=kwargs.get("enabledColour",self.enabledColour)
		self.enabledFG=kwargs.get("enabledFG",self.enabledFG)
		self.hoverColour=kwargs.get("hoverColour",self.hoverColour)
		self.clickedColour=kwargs.get("clickedColour",self.clickedColour)
		self.disabledColour=kwargs.get("disabledColour",self.disabledColour)
		self.disabledFG=kwargs.get("disabledFG",self.disabledFG)

		#Update state
		self.state=kwargs.get("state",self.state)

		#Update the widgets etc
		self.textLabel.config(font=self.font)
		self.textLabel.config(textvariable=self.textVar)
		#Only update colour if mouse is not over button
		if self.state:
			self.changeButtonColour(self.enabledColour)

	def changeButtonColour(self,bg,**kwargs):
		"""
		This method is used to change the buttons colour
		and change its background and text colour if needed
		temporarily only
		"""
		#Change the colours with overide True
		self.colour(bg,overide=True)
		self.textLabel.colour(bg)

	def pressBind(self,pressOrRelease):
		"""
		Function that handles button
		click release events and changes
		colour depending on what user is doing
		True = pressing
		False = release
		"""
		#Check button is active
		if self.state:
			#If user clicks button show clicked colour
			if pressOrRelease:
				self.pressing=True
				self.changeButtonColour(self.clickedColour)
			#When user releases mouse change back
			else:
				self.pressing=False
				self.changeButtonColour(self.hoverColour)

	def runCommand(self):
		"""
		This method will execute the command
		stored inside the button
		"""
		#Activate colour
		self.pressBind(True)
		#Check the button has a command
		if self.command and self.state:
			#Run the command using the external function
			runCommand(self.command,name="MainButton")

	def hover(self,inOut):
		"""
		This method is run when the mouse
		hovers over the button, depending
		on the state of the button it will change 
		colour
		True = In
		False = Out
		"""
		if self.state:
			#If the hover state is false then hover is not active
			if inOut:
				#Only change to hover if user isn't still pressing button
				if self.pressing == False:
					#Activate hover
					self.hoverOn=True
					#Change colour#
					self.changeButtonColour(self.hoverColour)
				else:
					self.pressBind(True)
			else:
				#Deactivate hover
				self.hoverOn=False
				#Change colours
				self.changeButtonColour(self.enabledColour)

	def changeState(self,TrueOrFalse):
		"""
		The change state method will change
		the state of the button.
		True = On
		False = Off 
		"""
		#Turn on
		if TrueOrFalse == True and self.state == False:
			self.state=True
			#Change colours
			self.changeButtonColour(self.enabledColour)
		#Turn off
		elif TrueOrFalse == False and self.state:
			self.state=False
			#Change colours
			self.changeButtonColour(self.disabledColour)
			self.textLabel.update(fg="#1BF293")

class mainLabel(Label):
	"""
	The main label widget is a custom
	label widget that is more advanced
	because it can change colour depending
	on its background and has more control
	over font etc.
	"""
	def __init__(self,parent,**kwargs):
		Label.__init__(self,parent)
		self.parent=parent
		#Store text data
		self.textVar=StringVar()
		self.textVar.set("mainLabel")
		#Store look of the label
		self.fg=None
		self.colourVar="#FFFFFF"
		self.font="Avenir 14"
		#Initiate update
		self.update(**kwargs)

	def update(self,**kwargs):
		"""
		The update method will allow the
		label to be changed with kwargs
		"""
		self.textVar.set(kwargs.get("text",self.textVar.get()))
		self.textVar=kwargs.get("textvariable",self.textVar)
		self.font=kwargs.get("font",self.font)
		self.fg=kwargs.get("fg",self.fg)
		self.colourVar=kwargs.get("colour",self.colourVar)
		#Update
		self.config(textvariable=self.textVar,font=self.font)
		if self.fg == None:
			self.colour(self.colourVar)
		else:
			self.config(fg=self.fg)

	def colour(self,background):
		"""
		The colour method will change the colour
		of the background and automatically 
		change text colour to suit
		"""
		self.config(bg=background)
		self.config(fg=getColourForBackground(background))

class advancedListbox(Listbox):
	"""
	The advanced Listbox class is a class that
	modifies the standard tkinter listbox
	but adds more customization and adds a scroll
	bar
	"""
	def __init__(self,parent,**kwargs):
		Listbox.__init__(self,parent)

		#Add a scrollbar
		self.scrollBar=Scrollbar(self)
		self.scrollBar.pack(side=RIGHT,fill=Y)
		self.scrollBar.config(command=self.yview)
		self.config(yscrollcommand=self.scrollBar.set)
		#Store ui
		self.font="Avenir 20"
		#Store objects
		self.data={}
		#Store names and colours
		self.colourData={}
		#Update
		self.updateListbox(**kwargs)

	def updateListbox(self,**kwargs):
		"""
		The update method to update
		any features of the listbox
		"""
		self.font=kwargs.get("font",self.font)
		#Update
		self.config(font=self.font)

	def addObject(self,displayName,object,**kwargs):
		"""
		This method will allow an object
		to be added to a listbox and 
		return the object instead of plain text
		"""
		#Get colour for listbox element
		colour=generateHexColour()
		colour=kwargs.get("colour",colour)
		#Add reference in dictionary
		self.data[displayName]=object
		self.colourData[displayName]=colour
		#Add to listbox
		self.insert(END,displayName)
		self.itemconfig(END,bg=colour)
		self.itemconfig(END,fg=getColourForBackground(colour))

	def updateObject(self,name,newObject):
		"""
		This method will update the object
		stored inside the listbox
		but keep the same key value
		"""
		if name in self.data:
			self.data[name]=newObject

	def getSelection(self,**kwargs):
		"""
		This method will return the item
		that is selected in the listbox,
		if the "basic" parameter is sent
		then the text it displays is returned
		else the object is returned
		"""
		#Basic is variable for if only text is returned
		basic=False
		basic=kwargs.get("basic",basic)

		#Attempt to get the current selection index
		currentSelectionIndex=self.curselection()

		if len(currentSelectionIndex) > 0:
			#Find matching text using index
			try:
				currentSelection=self.get(currentSelectionIndex[0])
			except:
				log.report("Error getting selection",tag="Error")
			else:
				#If only the text needs to be returned
				if basic:
					return currentSelection
				#If the object in dictionary needs to be returned
				else:
					return self.data[currentSelection]
		else:
			return None

	def secureClear(self):
		"""
		This method securely erases
		the data stored in the listbox
		and removes all text
		"""
		#Delte dicrionary keys
		self.data.clear()
		#Clear screen
		self.delete(0,END)

class advancedEntry(Entry):
	"""
	Modified entry that can
	contain placeholders and more
	"""
	def __init__(self,parent,placeHolder,**kwargs):
		Entry.__init__(self,parent,**kwargs)

		#Store Colour info
		self.placeHolder=placeHolder
		self.placeHolderColour="#BEC0B8"
		self.defaultColour="#000000"

		#Set up the placeholder
		self.placeHolderActive=True
		self.insert(END,placeHolder)
		self.config(fg=self.placeHolderColour)

		#Store the data
		self.data=StringVar()

		#Add bindings
		self.bind("<Button-1>",lambda event: self.updatePlaceHolder())

	def updatePlaceHolder(self):
		"""
		This method is called
		when the entry is clicked
		so the placeholder is removed
		and the settings are reset
		"""
		if self.placeHolderActive:
			#Remove content
			self.delete(0,END)
			#Change FG
			self.config(fg=self.defaultColour)
			#Change show
			self.config(show="•")
			#Update Variable
			self.placeHolderActive=False

	def getData(self):
		"""
		The method to return data from 
		the entry it ensures the placeholder
		is not returned
		"""
		if self.placeHolderActive:
			return None
		else:
			#Get the data
			data=self.get()
			if len(data.split()) > 0:
				return data
			else:
				return None

	def resetEntry(self):
		"""
		Reset the entry and 
		add the placeholder back
		to the entry
		"""
		#Clear Entry
		self.delete(0,END)
		#Change colour
		self.config(fg=self.placeHolderColour)
		#Change show
		self.config(show="")
		#Add placeholder
		self.insert(END,self.placeHolder)
		#Reset the variable
		self.placeHolderActive=True
#====================Secondary Classes====================
"""
Secondary classes are classes that inherit from the core classes
and are more program specific.
"""

class topLabel(mainFrame):
	"""
	The top strip class
	is a class which goes at 
	the top of a screen to
	show a message.
	"""
	def __init__(self,parent,**kwargs):
		mainFrame.__init__(self,parent)
		#Create center frame
		self.centerFrame=mainFrame(self)
		self.centerFrame.pack(expand=True)
		#Create Label
		self.textVar=StringVar()
		self.textVar.set("topLabel")
		self.textLabel=mainLabel(self.centerFrame,font="Avenir 20",textvariable=self.textVar)
		self.textLabel.pack(expand=True,fill=X)
		#Update
		self.updateLabel(**kwargs)

	def updateLabel(self,**kwargs):
		"""
		Update the strip with kwargs
		"""
		#Get Text
		self.textVar.set(kwargs.get("text",self.textVar.get()))
		self.textVar=kwargs.get("textvariable",self.textVar)
		#Update
		self.textLabel.update(textvariable=self.textVar)

class masterScreen:
	"""
	The master screen class
	is a class which is a parent
	for a screen it will store the 
	children and screen info.
	"""
	def __init__(self):
		self.lastScreen=None

class screen(mainFrame):
	"""
	The screenclass is a class
	for every screen in PyPassword.
	It is a frame that can be hidden and shown
	the screen will also store the preset
	context buttons 
	"""
	#Store last screen loaded
	lastScreen=None
	#Store the status variable
	statusVar=None
	#Store protected screens
	protectedScreens=[]
	def __init__(self,parent,screenName,**kwargs):
		mainFrame.__init__(self,parent)
		self.screenName=screenName
		#Store the context bar information
		self.context=None
		self.contextInfo={}
		#Does screen show sensitive info?
		self.protected=False
		#Store any commands that need to run when screen loaded
		self.screenCommands=[]

		#Update from kwargs
		self.protected=kwargs.get("protected",self.protected)
		#Update
		if self.protected:
			screen.protectedScreens.append(self)

	def show(self):
		"""
		The show method will show the screen,
		it does this by hiding the last used screen
		and showing the current screen
		"""
		#Stop screen being reloaded
		if screen.lastScreen != self:
			#Hide last screen
			if "pack_forget" in dir(screen.lastScreen):
				screen.lastScreen.pack_forget()

			#Show current screen
			self.pack(expand=True,fill=BOTH)
			#Update the status var
			if screen.statusVar:
				if type(screen.statusVar) == StringVar:
					screen.statusVar.set(self.screenName)
			#Set as last screen
			screen.lastScreen=self

			#Update context bar
			self.runContext()

			#Run any commands the screen has saved
			for command in self.screenCommands:
				runCommand(command,name="Screen Class")

	def addContextInfo(self,position,**kwargs):
		"""
		This function allows a screen
		to be configured to load certain context
		items when it is shown on screen
		"""
		self.contextInfo[position]=kwargs

	def updateCommand(self,position,**kwargs):
		"""
		This function updates any context bar 
		information stored in the screen class
		"""
		#Update the dictionary, the dictionary on right takes priority
		self.contextInfo[position] = {**self.contextInfo[position], **kwargs}

	def runContext(self):
		"""
		This is the method to update
		the context bar with the preset 
		commands that the screen stores
		"""
		#Update the contexts
		if type(self.context) == contextBar:
			numberOfButtons=len(self.contextInfo)
			if numberOfButtons > 0:
				#Set context to correct number of places
				self.context.setPlaceholders(numberOfButtons)
				#Add the context buttons
				for position in self.contextInfo:
					self.context.addButton(position,**self.contextInfo[position])
			else:
				self.context.resetBar()

		else:
			print("Not given a context bar")

	def addScreenCommand(self,command):
		"""
		This method will allow a command
		to be run when the screen is loaded
		"""
		if command not in self.screenCommands:
			self.screenCommands.append(command)

class contextBar(mainFrame):
	"""
	The contextBar class will be a class
	that stretches across the screen and has
	contextual buttons to execute. That can
	be swapped and modified to suit onscreen
	actions
	"""
	def __init__(self,parent,**kwargs):
		mainFrame.__init__(self,parent)
		#Preset bar colours, fonts etc
		self.font="Avenir 14"
		self.enabledColour="#E8EDEA"
		self.hoverColour="#DFE4E2"
		self.clickedColour="#C5F71C"
		self.defaultText=""
		#Store name and command in dictionary
		self.nameDict={}
		#The array that stores buttons
		self.buttonArray=[]
		#Store number of active sections
		self.sections=0
		#Section Types
		self.sectionTypes=["Button","Checkbutton"]

		#Generate preset placeholders
		self.presetPlaces=1
		self.presetPlaces=kwargs.get("places",self.presetPlaces)
		for x in range(self.presetPlaces):
			self.addPlaceholder()

		#Update
		self.mainAttributes={self.font:"font",self.enabledColour:"enabledColour",
		                     self.hoverColour:"hoverColour",self.clickedColour:"clickedColour"}
		self.updateBar(**kwargs)

	def updateBar(self,**kwargs):
		"""
		Update the bar with KWARGS
		"""
		#Get kwargs
		for att in self.mainAttributes:
			att=kwargs.get(self.mainAttributes[att],att)
		#Update
		for button in self.buttonArray:
			button.updateButton(font=self.font)

	def updateContextButton(self, index, **kwargs):
		"""
		This method will allow a
		certain button on the bar
		to be changed
		"""
		if index+1 <= len(self.buttonArray) and index >= 0:
			self.buttonArray[index].updateButton(**kwargs)

	def addPlaceholder(self):
		"""
		This method will add a section to 
		the context bar which can be used
		to add a button
		"""
		self.sections+=1
		#Create Button
		newButton=mainButton(self,enabledColour=self.enabledColour,
		                     hoverColour=self.hoverColour,text=self.defaultText)
		#Add button to array
		self.buttonArray.append(newButton)
		#Show the button on the bar itself
		newButton.pack(fill=X,expand=True,side=LEFT)

	def removePlaceholder(self,*index):
		"""
		This will remove a placeholder
		from the context bar, if an index
		is not specified the end button
		will be removed
		"""
		defaultIndex=0
		#If index is specified
		if len(index) > 0:
			#Set Default index
			defaultIndex=index[0]

		#Set default index as last item
		else:
			if len(self.buttonArray) > 0:
				defaultIndex=len(self.buttonArray)-1

		if defaultIndex+1 <= len(self.buttonArray) and defaultIndex >= 0:
			#Destroy the widget and remove from array
			self.buttonArray[defaultIndex].destroy()
			#Remove from array
			del self.buttonArray[defaultIndex]

	def addButton(self,index,**kwargs):
		"""
		This method allows a button to be added
		to the context bar
		"""
		if index+1 <= len(self.buttonArray) and index >= 0:

			#Ensures a disabled button doesn't stay disabled when used again
			butState=True
			butState=kwargs.get("state",butState)
			newKwargs={**kwargs,**{"state":butState}}
			#Rest the button and add new kwargs
			self.resetButton(index)
			self.buttonArray[index].updateButton(**newKwargs)

	def setPlaceholders(self,numberOfPlaceHolders):
		"""
		This method sets the context bar
		to the exact number of placeholders
		"""
		numberOfButtons=len(self.buttonArray)
		if numberOfButtons != numberOfPlaceHolders:
			diff=numberOfButtons-numberOfPlaceHolders
			#Iterate through modulus of difference
			for x in range(abs(diff)):
				#Buttons need to be removed
				if diff > 0:
					self.removePlaceholder()
				#Buttons are added
				else:
					self.addPlaceholder()

	def resetBar(self):
		"""
		This method resets all the buttons
		and removes commands
		"""
		for x in range(0,len(self.buttonArray)):
			self.resetButton(x)

	def resetButton(self,index):
		"""
		This method will reset
		the colours and hover colours
		of all the bar buttons, this is so
		colours don't overwrite new buttons
		"""
		if index+1 <= len(self.buttonArray) and index >= 0:
			self.buttonArray[index].updateButton(enabledColour=self.enabledColour,
			                                            hoverColour=self.hoverColour,
			                                            clickedColour=self.clickedColour,
			                                            text=self.defaultText,
			                                            command=None)
			#Ensures the button isn't still being pressed when context changes
			self.buttonArray[index].pressBind(False)

class advancedNotebook(mainFrame):
	"""
	The advanced notebook class
	is a class used to display
	multiple tabs and allow the user
	to navigate using tabs.
	"""
	def __init__(self,parent,**kwargs):
		mainFrame.__init__(self,parent)

		#The tab
		self.tabFrame=mainFrame(self)
		self.tabFrame.pack(side=TOP,fill=X)

		self.tabFrame.colour("#BDC7C5")

		#Selection bar
		self.selectionBar=selectionBar(self.tabFrame)
		self.selectionBar.pack(expand=True)

		#Store a dictionary of tabs and frames
		self.pages={}
		self.pageList=[]

		#Store tab counter
		self.tabCounter=-1

		#Store currently loaded frame and button
		self.currentFrame=None

	def addPage(self,tabName,pageFrame,**kwargs):
		"""
		This method will add a tab
		to the advanced notebook.
		It will display a certain
		screen when displayed
		"""
		#Add the page to the dictionary
		self.pages[tabName]=pageFrame
		#Increase counter by one
		self.tabCounter+=1
		index=self.tabCounter
		index=kwargs.get("index",index)

		if tabName not in self.pageList:
			self.pageList.append(tabName)
			#Add a bar to the self
			self.selectionBar.addTab(index,tabName,lambda tab=tabName: self.loadFrame(tab))

	def loadFrame(self,tabName):
		"""
		Load frames function
		"""
		#Get the correct frame to load
		frameToLoad=self.pages[tabName]

		#Hide the current frame
		if self.currentFrame:
			self.currentFrame.pack_forget()

		#Show the new frame
		frameToLoad.pack(expand=True,fill=BOTH)
		#Set as current
		self.currentFrame=frameToLoad




class podNotebook(advancedNotebook):
	"""
	The pod notebook is a special
	notebook for viewing pod 
	information. It handles loading and 
	displaying pod data
	"""
	def __init__(self,parent,**kwargs):
		advancedNotebook.__init__(self,parent,**kwargs)

	def loadTemplate(self,templateName):
		"""
		This function will load a 
		certain pod template to the notebook
		so its ready to show a users data
		"""
		print("Ready to load template",templateName)

class selectionBar(mainFrame):
	"""
	The selection bar
	is a bar that allows a single 
	selection. This can be used
	to naivgate etc.
	"""
	def __init__(self,parent,**kwargs):
		mainFrame.__init__(self,parent,**kwargs)

		#Store colours
		self.selectedTabColour="#1BF293"
		self.notselectedTabColour="#DFEDEA"
		self.hoverColour="#F9FFFC"

		#Store current tab
		self.currentTab=None

		#Store the tabs
		self.tabCommandDict={}
		self.tabDict={}
		self.tabList=[]

		#How many placeholders are setup initially
		self.initialPlaces=0
		self.initialPlaces=kwargs.get("places",self.initialPlaces)

		for x in range(self.initialPlaces):
			self.addPlace()

	def addPlace(self):
		"""
		This method will allow a tab
		to be added to the frame
		"""
		#Create Button
		newButton=mainButton(self)
		newButton.pack(fill=BOTH,expand=True,side=LEFT)
		#Add to list
		self.tabList.append(newButton)

	def addTab(self,index,tabName,command):
		"""
		This method allows a tab to
		be added to the selection bar
		"""
		#Add reference
		self.tabCommandDict[tabName]=command
		if index+1 > len(self.tabList):
			self.addPlace()
		if index >= 0:
			#Get the correct button
			button=self.tabList[index]
			#Add a reference
			self.tabDict[tabName]=button
			#Update the button to correct info
			button.updateButton(text=tabName,command=lambda: self.runTabCommand(tabName))
			#If this is the first tab run it so the notebook is showing something
			if index == 0:
				self.runTabCommand(tabName)
	def runTabCommand(self,tabName):
		"""
		This function overrides the commands
		of all the tabs so it can handle things
		such as colour change etc. 
		"""
		if tabName != self.currentTab:
			#Get the correct command for that name
			buttonCommand=self.tabCommandDict[tabName]

			#Run the commmand
			buttonCommand()

			#Change other colours
			if self.currentTab:
				self.tabDict[self.currentTab].updateButton(enabledColour=self.notselectedTabColour,
				                                           hoverColour=self.hoverColour,
				                                           clickedColour=self.notselectedTabColour)

			##Change the colour
			selectButton=self.tabDict[tabName]
			selectButton.updateButton(enabledColour=self.selectedTabColour,
			                          hoverColour=self.selectedTabColour,
			                          clickedColour=self.selectedTabColour)
			#Update the current tab
			self.currentTab=tabName

	def removePlace(self,index):
		"""
		This function will allow
		a tab to be removed from the bar
		"""
		#Find correct index in the list
		if index <= len(self.tabList)-1:
			place=self.tabList[index]
			#Remove from array
			self.tabList.remove(place)
			#Remove from the dictionary
			for item in self.tabDict:
				if self.tabDict[item] == place:
					del self.tabDict[item]
					break
			#Remove the widget
			place.pack_forget()









#====================Non UI Classes====================
"""
The non ui classes are classes that are not based on 
tkinter widgets.
"""

class podTemplate:
	"""
	The pod template 
	is a class which can be used
	to represent what kind of data
	is stored in a pod.
	"""
	#Store the templates and corresponding colours
	templateColours={}

	def __init__(self,templateName,templateColour):
		#Name and Colour of template
		self.templateName=templateName
		self.templateColour=templateColour

		#Store valid data types
		self.validDataTypes=[Entry,advancedEntry,Text,OptionMenu]

		#Store the tabs
		self.tabs={}

		#Add to dict
		podTemplate.templateColours[self.templateName]=self.templateColour

	def addTab(self,tabName):
		"""
		This method allows a tab to be
		easily added to the template which is
		an area to store data.
		"""
		#Initiate an empty dictionary in the tab dictionary
		self.tabs[tabName]={}

	def addTemplateSection(self,tabName,sectionName,dataType,buttonList,**kwargs):
		"""
		This method allows a section of data to be added to the template.
		For example a section for "Password" or "Email" 
		"""
		if tabName in self.tabs:
			#Get section colour
			sectionColour="#FFFFFF"
			sectionColour=kwargs.get("colour",sectionColour)
			#Check if dataType is valid
			if dataType not in self.validDataTypes:
				dataType=Entry
				log.report("Changed data type for",sectionName)
			#Add the data to list
			dataArray=[sectionName,dataType,buttonList,sectionColour]
			#Add list to dictionary
			self.tabs[tabName]=dataArray


#====================Create the pod templates====================


#=====Login======
loginTemplate=podTemplate("Login","#3CE995")
loginTemplate.addTab("Login")
loginTemplate.addTab("Advanced")

#loginTemplate.addTemplateSection("Login","Username",Entry)

#=====Secure Note======
secureNoteTemplate=podTemplate("SecureNote","#56B6C4")






