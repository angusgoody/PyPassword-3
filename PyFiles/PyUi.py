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
from tkinter import ttk
from PEM import *
from random import randint
import webbrowser
#====================Log====================

log=logClass("User Interface")
#====================Preset variables====================
mainRedColour="#EE687F"
mainGreenColour="#A9F955"
mainOrangeColour="#E7A136"
mainBlueColour="#17F388"
mainGreyColour="#CDD7D6"
mainClickedColour="#A9F955"
mainWhiteColour="#E8EDEA"
mainLockedColour="#685DE3"

mainSecondOrangeColour="#D89633"
mainSecondBlueColour="#13C770"
mainSecondGreenColour="#7CCE32"
mainSecondRedColour="#A25360"
mainSecondGreyColour="#8B8F8F"

#Store variables for all programs
mainVars={}
#====================Functions====================
"""
This section is for functions that aid with the user
interface elements of PyPassword
"""
#Utility functions
def smallCheck(dataToFind,dataSource,capital,fullCheck):
	"""
	The basic search function
	which will check to see
	if two parameters are equal
	
	capital = True = ignore case
	fullCheck = True = exact matches
	"""
	#If both dataToFind and source are string
	if type(dataToFind) is str and type(dataSource) is str:
		#If capitals do not matter
		if capital:
			#If exact matches are needed
			if fullCheck:
				if dataToFind.upper() == dataSource.upper():
					return True
				else:
					return False
			#If exact matches are not needed
			else:
				#By using "in" can find matches in parts of words
				if dataToFind.upper() in dataSource.upper():
					return True
				else:
					return False

	#Comparison for non string values such as objects etc
	if fullCheck:
		if dataToFind == dataSource:
			return True
		else:
			return False
	else:
		if dataToFind in dataSource:
			return True
		else:
			return False

def searchDataSource(dataToFind,dataSource,**kwargs):
	"""
	Search function
	for finding data inside
	a data structure 
	"""
	#Check for kwargs
	capital=True
	capital=kwargs.get("capital",capital)
	fullCheck=True
	fullCheck=kwargs.get("full",fullCheck)

	#Iterate through data source
	for item in dataSource:

		#If the type is dictionary or list
		if type(item) == list or type(item) == dict:
			#Search the items in the list or dictionary keys
			result=searchDataSource(dataToFind,item,capital=capital)
			if result:
				return result
		#If dictionary
		if type(dataSource) is dict:
			#Search the values in the dictionary instead of just keys
			result=searchDataSource(dataToFind,dataSource.values(),capital=capital)
			if result:
				return result
		#If recursion is not possible just do a simple compairsion
		else:
			result=smallCheck(dataToFind,item,capital,fullCheck)
			if result:
				return result

	return False

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
	try:
		content=command()
	except Exception as e:
		print("Error running command",identifier,e,command)
		log.report("Error executing command through function",e,command,tag="Error")
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

def addDataToWidget(widget,data):
	"""
	Function to add data to a variety
	of widgets 
	"""
	validWidgets=[Entry,mainLabel,Text,advancedEntry]
	widgetType=type(widget)
	#Check widget type
	if widgetType in validWidgets:
		#Add to Entry
		if widgetType == Entry or widgetType == advancedEntry:
			widget.delete(0,END)
			widget.insert(END,data)
		#Add to type Text
		elif widgetType == Text:
			widget.delete("1.0",END)
			widget.insert("1.0",data)
		#Add to type mainLabel
		elif widgetType == mainLabel:
			widget.textVar.set(data)
	else:
		log.report("Non supported widget used to add data",type(widget))

def getDataFromWidget(widget):
	"""
	Function to get data
	from a range of widgets 
	"""
	validWidgets=[Entry,mainLabel,Text,OptionMenu,advancedEntry]
	widgetType=type(widget)
	if widgetType in validWidgets:
		if widgetType == Entry or widgetType == advancedEntry:
			return widget.get()
		elif widgetType == Text:
			return widget.get("1.0",END)
		elif widgetType == mainLabel:
			return widget.textVar.get()
		elif widgetType == advancedOptionMenu:
			return widget.var.get()
	else:
		log.report("Attempt to get info from non supported widget",widgetType)

def changeWidgetState(widget,state):
	"""
	Function to update
	state of a range
	of diffrent widgets
	"""
	#Get the type of widget
	widgetType=type(widget)
	validWidgets=[Entry,advancedEntry,Text]

	#Change the state
	if widgetType in validWidgets:
		widget.config(state=state)
		if widgetType == Text:
			if state == DISABLED:
				widget.config(fg="#474846")
			else:
				widget.config(fg="#000000")

def loadWebsite(address):
	"""
	Load a website with a certain address
	"""
	httpCheck=False
	wwwCheck=False
	if address:
		if len(address.split()) > 0:
			#Check for a prefix
			if "https://" in address or "http://" in address:
				httpCheck=True
			else:
				if "www." in address:
					wwwCheck=True

			#Add if needed
			if wwwCheck == False:
				address="www."+str(address)
			if httpCheck == False:
				address="https://"+str(address)

			#Add the www
			try:
				webbrowser.open_new(address)
			except:
				showMessage("Error","Could not open address")
				log.report("Error opening address",tag="Error")
			else:
				log.report("Opened web page")

def copyToClipboard(data):
	"""
	Will copy data to
	the computers clipboard
	ready to paste anywhere
	"""

	if len(str(data).split()) > 0:
		if "window" in mainVars:
			mainWindow=mainVars["window"]
			mainWindow.clipboard_clear()
			mainWindow.clipboard_append(data)
			log.report("Added data to clipboard")
			showMessage("Data copied","Data copied to clipboard")
	else:
		showMessage("No data","No data to copy")

#Recursion
def recursiveBind(parent,bindButton,bindFunction,**kwargs):
	"""
	This function will bind a function
	recursively to a widget, this means
	all the children of the widget
	will also be binded to the same function
	"""
	#Bind the parent
	parent.bind(bindButton,bindFunction)
	#Check if the parent has children
	if "winfo_children" in dir(parent):
		#Bind the children
		for child in parent.winfo_children():
			recursiveBind(child,bindButton,bindFunction)
	else:
		try:
			parent.bind(bindButton,bindFunction)
		except Exception as e:
			log.report("Could not bind function to",e,type(parent),tag="Error")

def basicChangeColour(widget,colour):
	#Items who's highlight background is changed
	highlightItems=[Entry,advancedEntry,Button,Text,Listbox,OptionMenu]
	labelItems=[Label,mainLabel]
	#Change colour
	if type(widget) in highlightItems:
		widget.config(highlightbackground=colour)
	elif type(widget) in labelItems:
		widget.config(bg=colour)
		widget.config(fg=getColourForBackground(colour))
	else:
		widget.config(bg=colour)

def recursiveColour(parent, colour, **kwargs):
	"""
	The recursive colour function
	will change the colour of widgets
	recursively
	"""
	#Items to exclude
	excludeItems=[ttk.Scale]

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
		self.mouseInside=False
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
		#self.addBinding("<Button-1>",lambda event: self.runCommand())
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
				#Run command if mouse is over button
				if self.mouseInside:
					self.runCommand()

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
			self.mouseInside=inOut
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
			#Change the foreground colour
			self.textLabel.config(fg=self.disabledFG)

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
		self.width=None
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
		self.width=kwargs.get("width",self.width)
		#Update
		if self.width:
			self.config(textvariable=self.textVar,font=self.font,width=self.width)
		else:
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
			except Exception as e:
				log.report("Error getting selection",e,tag="Error")
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

	def addExisting(self,objectKey):
		"""
		This function adds 
		an existing object back
		into the listbox with just
		a name.
		"""
		if objectKey in self.data:
			self.insert(END,objectKey)
			#Update the colour
			if objectKey in self.colourData:
				self.itemconfig(END,bg=self.colourData[objectKey])

	def restoreData(self):
		"""
		Restore all the data back to the screen
		"""
		self.delete(0,END)
		for item in self.data:
			self.addExisting(item)

class advancedEntry(Entry):
	"""
	Modified entry that can
	contain placeholders and more
	"""
	def __init__(self,parent,placeHolder,hide,**kwargs):
		Entry.__init__(self,parent,**kwargs)
		self.parent=parent
		self.hide=hide

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
		self.bind("<FocusOut>",lambda event: self.clickOff())

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
			if self.hide:
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

	def clickOff(self):
		"""
		When the user clicks off the entry
		will put placeholder back if the content
		of the entry is empty
		"""
		if len(self.get().split()) < 1:
			self.resetEntry()
		self.parent.focus()

class dataWindow(Toplevel):
	"""
	The data window is a top
	level window that allows
	user to enter and input data
	and the class will store and return
	data.
	"""

	def __init__(self,root,name,**kwargs):
		Toplevel.__init__(self,root)
		#Variables
		self.master=root
		self.name=name
		#Configure window
		self.title=self.name
		self.geometry("400x200")
		#Status
		self.status=mainLabel(self,font="Avenir 15")
		self.status.pack(side=BOTTOM,fill=X)
		self.status.textVar.set(self.name)
		self.status.colour("#3F5B65")
		#Context bar
		self.context=contextBar(self,places=2)
		self.context.pack(side=BOTTOM,fill=X)
		self.context.addButton(0,text="Cancel",enabledColour=mainRedColour)
		self.context.addButton(1,text="Create",enabledColour=mainBlueColour)
		self.context.getButton("Create").changeState(False)
		self.context.updateContextButton(0,command=lambda: self.quit())
		#Display label
		self.displayVar=StringVar()
		self.displayVar.set("Please enter data")
		self.displayWidget=None

		#Store the inputs
		self.inputWidgets={}
		self.inputCannotContain={}
		self.inputLengths={} #index 0 is min index 1 is max
		self.inputData={}

		#Run
		self.runWindow()

	def runWindow(self):
		"""
		Running a window will
		set the program focus to the popup
		window so the user cannot interact with
		the program.
		"""

		self.focus_set()
		self.grab_set()
		self.transient(self.master)
		self.resizable(width=False,height=False)

	def addDisplayLabel(self,widget):
		"""
		Will add a display label widget
		to the class and handle
		string variables and updating etc 
		"""
		self.displayWidget=widget
		widget.config(textvariable=self.displayVar)

	def addDataSource(self,widget,name,**kwargs):
		"""
		Add a data source widget to the class
		"""
		minLength=1
		maxLength=30
		cannotContain=[]
		minLength=kwargs.get("minLength",minLength)
		maxLength=kwargs.get("maxLength",maxLength)
		cannotContain=kwargs.get("cannotContain",cannotContain)
		#Add a reference
		self.inputWidgets[name]=widget
		#Add the kwargs
		self.inputCannotContain[name]=cannotContain
		self.inputLengths[name]=[minLength,maxLength]

		widgetType=type(widget)
		#Bind the widget
		if widgetType in [advancedEntry,Entry]:
			widget.bind("<KeyRelease>",lambda event: self.runCheck(name))
		else:
			if widgetType is StringVar:
				self.inputData[name]=widget

	def runCheck(self,identifier):
		"""
		This function will check
		the contents of a input
		to validate it against the specified requirements 
		"""
		validWidgets=[Entry,advancedEntry]
		if identifier in self.inputWidgets:
			correctWidget=self.inputWidgets[identifier]
			if type(correctWidget) in validWidgets:
				#Collect the required data
				requiredMinLength=self.inputLengths[identifier][0]
				requiredMaxLength=self.inputLengths[identifier][1]
				requiredCannotContain=self.inputCannotContain[identifier]
				#Get the data from the widget
				widgetData=getDataFromWidget(correctWidget)
				if widgetData:
					widgetDataLength=len(widgetData)
					#Check the length
					if widgetDataLength < requiredMinLength:
						self.updateCheck(identifier,"Please enter at least "+str(requiredMinLength)+" characters")
						#End
						return False
					if widgetDataLength > requiredMaxLength:
						self.updateCheck(identifier,"Please enter at the most "+str(requiredMaxLength)+" characters")
						#End
						return False
					#Check to see if it contains forbidden items
					if searchDataSource(widgetData,requiredCannotContain,capital=True):
						self.updateCheck(identifier,"Name is taken, please enter another")
						#End
						return False
				else:
					self.updateCheck(identifier,"Please enter data")
					#End
					return False

			#If the data is valid
			self.updateCheck(identifier,True)

	def updateCheck(self,identifier,message):
		"""
		Update the window
		based on what the user entered
		"""
		if message == True:
			#Enable the button to continue
			self.displayVar.set("Valid name")
			self.context.getButton("Create").changeState(True)
			#Store the data
			self.inputData[identifier]=getDataFromWidget(self.inputWidgets[identifier])
		else:
			#Disable the button to continue
			self.context.getButton("Create").changeState(False)
			self.displayVar.set(message)

	def quit(self):
		"""
		The quit method which
		will destroy the window
		and any saving etc.
		"""
		self.destroy()

	def getData(self):
		"""
		Function to return the stored data in the
		input areas of the data window
		"""
		return self.inputData

	def storeWidgetData(self,widgetName):
		"""
		Method is used to
		store the data
		from a widget inside the class
		"""
		if widgetName in self.inputWidgets:
			data=getDataFromWidget(self.inputWidgets[widgetName])
			self.inputData[widgetName]=data

class advancedOptionMenu(OptionMenu):
	"""
	Option Menu which allows
	the variable to accessed at any time
	"""
	def __init__(self,parent,variable,*values,**kwargs):
		OptionMenu.__init__(self,parent,variable,*values,**kwargs)
		self.var=variable
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

	#Store the menus to load
	publicMenu=None
	privateMenu=None

	def __init__(self,parent,screenName,**kwargs):
		mainFrame.__init__(self,parent)
		self.screenName=screenName
		self.parent=parent
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

			#Update the menu
			if self.protected == True:
				#Load the private menu
				if self.privateMenu:
					self.parent.config(menu=self.privateMenu)
			else:
				if self.publicMenu:
					self.parent.config(menu=self.publicMenu)

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
		self.enabledColour=mainWhiteColour
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


		#Update
		self.storedKwargs=None
		self.mainAttributes={self.font:"font",self.enabledColour:"enabledColour",
		                     self.hoverColour:"hoverColour",self.clickedColour:"clickedColour"}
		self.updateBar(**kwargs)


		#Generate preset placeholders
		self.presetPlaces=1
		self.presetPlaces=kwargs.get("places",self.presetPlaces)
		for x in range(self.presetPlaces):
			self.addPlaceholder()

	def updateBar(self,**kwargs):
		"""
		Update the bar with KWARGS
		"""
		#Get kwargs
		for att in self.mainAttributes:
			att=kwargs.get(self.mainAttributes[att],att)
		#Update
		for button in self.buttonArray:
			button.updateButton(**kwargs)
		#Update the store kwargs
		self.storedKwargs=kwargs

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
		newButton=mainButton(self,**self.storedKwargs)
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

	def getButtonIndex(self,buttonName):
		"""
		Return the index of a button by
		the name passed
		"""
		for button in self.buttonArray:
			currentButtonName=button.textVar.get()
			if buttonName == currentButtonName:
				buttonIndex=self.buttonArray.index(button)
				return buttonIndex

	def getButton(self,buttonName):
		"""
		This function will return the 
		button widget itself
		"""
		for button in self.buttonArray:
			if button.textVar.get() == buttonName:
				return button

class privateSection(mainFrame):
	"""
	The private section is a frame
	which will hold a section
	of users data. It will have a label which
	indicates the name of the data and then have ways
	for the user to interact with the data.
	"""
	validWidgets=[mainLabel,Label,Entry,advancedEntry,OptionMenu,Text]
	def __init__(self,parent):
		mainFrame.__init__(self,parent)

		#-----Widgets------

		#Container to manage the widgets
		self.container=mainFrame(self)
		self.labelFrame=mainFrame(self.container)
		self.widgetFrame=mainFrame(self.container)
		self.buttonFrame=mainFrame(self.container)

		#Label
		self.textVar=StringVar()
		self.textLabel=mainLabel(self.labelFrame,textvariable=self.textVar,font="Avenir 13",width=15)
		self.textLabel.pack(expand=True)
		#Context bar
		self.contextKwargs={"font":"Avenir 10","clickedColour":mainBlueColour}
		self.context=contextBar(self.buttonFrame,**self.contextKwargs)
		self.context.pack(expand=True)


		#-----Widgets------
		self.loadedWidget=None #String Value
		self.defaultWidget=mainLabel
		self.editWidget=Entry
		self.widgetFont="Avenir 16"
		self.widgetWidth=20

		self.savedWidgets={}
		self.savedWidgetData={}
		self.widgetVar=StringVar()
		self.widgetVar.set("Widget")

		self.hideData=False #Should data be hidden on startup
		#-----States-------
		self.hiddenState=False # False = Showing
		self.widgetState=None # False = Normal

	def displayWidget(self,widgetInstance):
		"""
		The function to actually configure
		the container to display
		the correct widget 
		"""
		widgetType=type(widgetInstance)
		#Organise container
		if widgetType == Text:
			self.container.pack(expand=True,fill=BOTH)
			self.labelFrame.grid(row=0,column=0,sticky=EW,pady=2)
			self.widgetFrame.grid(row=2,column=0,sticky=NSEW,padx=0)
			self.buttonFrame.grid(row=1,column=0,sticky=EW,pady=5)
			#Grid configure
			self.container.columnconfigure(0,weight=1)
			self.container.rowconfigure(2,weight=1)
			#Display text widget
			widgetInstance.pack(fill=BOTH,expand=True)
		else:
			self.container.pack(expand=True)
			self.labelFrame.grid(row=0,column=0,padx=5)
			self.widgetFrame.grid(row=0,column=1,padx=5)
			self.buttonFrame.grid(row=0,column=2,padx=5)
			#Display the other widget
			widgetInstance.pack(fill=X)

	def loadWidget(self,widgetName):
		"""
		This method allows different
		 types of widgets to be loaded
		 onto the frame
		"""
		#Check same widget is not loaded again
		if widgetName != self.loadedWidget:

			#Hide the current
			if self.loadedWidget:
				self.savedWidgets[self.loadedWidget].pack_forget()

			#Check if the widget is stored in memory
			if widgetName in self.savedWidgets:
				correctWidget=self.savedWidgets[widgetName]
				self.displayWidget(correctWidget)

			#Otherwise generate one and display it
			elif widgetName in privateSection.validWidgets:
				if widgetName == Entry:
					newWidget=Entry(self.widgetFrame,font=self.widgetFont,width=self.widgetWidth)
				elif widgetName == Text:
					newWidget=Text(self.widgetFrame,height=12,font=self.widgetFont,bg="#E2E9F0")
				elif widgetName == OptionMenu:
					newWidget=advancedOptionMenu(self.widgetFrame,self.widgetVar,self.widgetVar.get())
				else:
					newWidget=mainLabel(self.widgetFrame,font=self.widgetFont,width=self.widgetWidth)

				#Colour to match background colour
				basicChangeColour(newWidget,self.cget("bg"))
				#Add the widget to dict
				self.savedWidgets[widgetName]=newWidget
				#Display
				self.displayWidget(newWidget)

			#Update variable
			self.loadedWidget=widgetName
		else:
			log.report("Attempt to load same widget: ",widgetName)

	def addData(self,data,**kwargs):
		"""
		This function will add
		data to the current widget
		in the private section
		"""
		#Get a widget name to add to
		currentWidgetName=self.loadedWidget
		currentWidgetName=kwargs.get("widget",currentWidgetName)
		#Find the corresponding widget
		widget=self.savedWidgets[currentWidgetName]
		#Add data from chosen widget
		if currentWidgetName in self.savedWidgets:
			addDataToWidget(widget,data)
			#Store data
			self.savedWidgetData[currentWidgetName]=data

	def clearData(self,**kwargs):
		"""
		The method to remove data from the
		private section. kwargs
		specify if all the widgets
		need to be clear and if stored data
		needs to be removed
		"""
		#Collect kwargs
		allWidgets=False
		widgetData=False
		allWidgets=kwargs.get("allWidgets",allWidgets)
		widgetData=kwargs.get("widgetData",widgetData)

		if allWidgets:
			for widgetName in self.savedWidgets:
				#Remove the data from widget
				currentWidget=self.savedWidgets[widgetName]
				addDataToWidget(currentWidget,"")
				if widgetData:
					#Remove the stored data
					if widgetName in self.savedWidgetData:
						self.savedWidgetData[widgetName]=""

		#Clear only the loaded widget
		else:
			if self.loadedWidget in self.savedWidgets:
				addDataToWidget(self.savedWidgets[self.loadedWidget],"")
				if widgetData and self.loadedWidget in self.savedWidgetData:
					self.savedWidgetData[self.loadedWidget]=""

	def getData(self,**kwargs):
		"""
		Will get the data from
		a widget. specific 
		widget can be specified 
		and stored or raw.
		Raw = currently in widget 
		"""
		stored=False
		widget=self.savedWidgets[self.loadedWidget]
		widget=kwargs.get("widget",widget)
		stored=kwargs.get("stored",stored)

		widgetType=type(widget)

		#If the data is got from stored memory
		if stored:
			if widgetType in self.savedWidgetData:
				data=self.savedWidgetData[widgetType]
			else:
				data=None
		#If data is straight from widget
		else:
			data=getDataFromWidget(widget)

		return data

	def addContextCommand(self,index,buttonName,**kwargs):
		"""
		This function will add
		a button to the context bar
		of the private section
		"""
		#Copy to clipboard command
		if buttonName == "Copy":
			self.context.addButton(index,text=buttonName,**self.contextKwargs)
		#Hide data
		elif buttonName == "Hide":
			self.context.addButton(index,text=buttonName,command=lambda: self.toggleHide(),**self.contextKwargs)
		#Launch a website
		elif buttonName == "Launch":
			self.context.addButton(index,text=buttonName,command=lambda: loadWebsite(self.getData(stored=True)),**self.contextKwargs)
		#Generate a password for the entry
		elif buttonName == "Generate":
			self.context.addButton(index,text=buttonName,**self.contextKwargs)
		#Not specified do nothing
		else:
			self.context.addButton(index,text=buttonName,**self.contextKwargs)

	def hideWidget(self,widget,hideOrShow):
		"""
		This method actually changes
		the data in the widget
		"""
		widgetType=type(widget)
		if widgetType in [Entry,mainLabel]:

			#Entry
			if widgetType == Entry:
				if hideOrShow == "Hide":
					widget.config(show="•")
				else:
					widget.config(show="")

			#MainLabel
			elif widgetType == mainLabel:
				if hideOrShow == "Hide":
					widget.textVar.set("••••••••")
				else:
					if mainLabel in self.savedWidgetData:
						widget.textVar.set(self.savedWidgetData[mainLabel])
					else:
						log.report("No data found to display on mainLabel")

	def toggleHide(self,**kwargs):
		"""
		This function will change the 
		contents of the section to be hidden
		or showing.
		False = Showing
		True = Hidden
		"""
		currentCommand=None
		forced=None
		#Determine default
		if self.hiddenState == False:
			currentCommand=True
			self.hiddenState=True

		elif self.hiddenState == True:
			currentCommand=False
			self.hiddenState=False

		#Check for kwargs
		forced=kwargs.get("forced",forced)
		if forced:
			currentCommand=forced
			if forced == False:
				self.hiddenState=False
			elif forced:
				self.hiddenState=True

		#Check data needs to be hidden
		if currentCommand is not None:
			#Show the data
			if currentCommand == False:
				for widget in self.savedWidgets:
					self.hideWidget(self.savedWidgets[widget],"Show")
				#Update the button
				but=self.context.getButton("Show")
				if but:
					but.textVar.set("Hide")


			#Hide the data
			elif currentCommand == True:
				for widget in self.savedWidgets:
					self.hideWidget(self.savedWidgets[widget],"Hide")
				#Update the button
				but=self.context.getButton("Hide")
				if but:
					but.textVar.set("Show")

	def changeState(self,chosenState):
		"""
		Disable or enable the section
		False = Normal
		True = Disabled
		"""
		#So when program first runs None is changed
		if self.widgetState == None:
			self.widgetState = not chosenState

		#Disable
		if chosenState == True and self.widgetState == False:
			for widget in self.savedWidgets:
				changeWidgetState(self.savedWidgets[widget],DISABLED)
			#Enable the hide button
			button=self.context.getButton("Hide")
			if button:
				button.changeState(True)

			#Hide the password
			if self.hideData:
				self.toggleHide(forced=False)

			#Update the var
			self.widgetState=True

		#Enable
		elif chosenState == False and self.widgetState == True:
			for widget in self.savedWidgets:
				changeWidgetState(self.savedWidgets[widget],NORMAL)
			#Ensure that data can be viewed
			if self.hiddenState:
				self.toggleHide(forced=False)
			#Disable the hide button
			button=self.context.getButton("Hide")
			if button:
				button.changeState(False)
			#Update the var
			self.widgetState=False

	def restoreData(self,widgetName):
		"""
		This method will restore
		the data inside a certain saved
		widget. This removes data
		in the widget and replaces it with
		saved data
		"""
		if widgetName in self.savedWidgets:
			widget=self.savedWidgets[widgetName]
			#Clear the widget
			addDataToWidget(widget,"")
			#Restore
			if widgetName in self.savedWidgetData:
				addDataToWidget(widget,self.savedWidgetData[widgetName])
				log.report("Restored data for widget",widgetName)

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
		#Get the index
		index=None
		index=kwargs.get("index",index)
		#Add a bar to the self
		self.selectionBar.addTab(tabName,command=lambda tab=tabName: self.loadFrame(tab),index=index)

	def loadFrame(self,tabName):
		"""
		This function will load a frame.
		The parameter tabName indicates the 
		correct frame that should be displayed
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

		#Store templates that have already been generated
		self.savedTemplates={}
		#Store current template
		self.currentTemplate=None
		#Store the sections
		self.sectionDict={}
		#Store state
		self.notebookState=None #False = Normal True = Disabled

	def addPage(self,tabName,pageFrame,**kwargs):
		return super(podNotebook, self).addPage(tabName,pageFrame,**kwargs)

	def loadTemplate(self,templateName):
		"""
		This function will load a
		certain pod template to the notebook
		so its ready to show a users data
		"""
		#Get the correct template
		correctTemplate=podTemplate.templates[templateName]
		log.report("Loading template",correctTemplate)

		#First stop loading the same template
		if self.currentTemplate != templateName:
			#Attempt to load from memory
			if templateName in self.savedTemplates:
				log.report("A template was loaded from memory",templateName)
				#Get the stored widgets from memory
				templateArray=self.savedTemplates[templateName]
				#Get the template info from the class
				correctTemplate=podTemplate.templates[templateName]
				#Set the selection bar
				self.selectionBar.setSize(len(correctTemplate.tabs))

				#Load the tabs
				counter=0
				for tabList in templateArray:
					tabName=tabList[0]
					tabFrame=tabList[1]
					#Add the frame to the correct tab
					self.addPage(tabName,tabFrame,index=counter)
					counter+=1

				#Update the variable
				self.currentTemplate=templateName

			#Need to generate a new section
			else:

				#Check its a valid pod
				if templateName in podTemplate.templates:
					log.report("A template was generated",templateName)

					#First get the template information
					correctTemplate=podTemplate.templates[templateName]

					#Initalise an array to store data
					self.savedTemplates[templateName]=[]

					#Iterate through the template
					for tabName in correctTemplate.tabOrder:
						#Initialise array
						currentTemplateArray=["","",{}]
						self.savedTemplates[templateName].append(currentTemplateArray)
						#Create a new frame
						newFrame=mainFrame(self)
						#Get the widget list
						sectionList=correctTemplate.tabs[tabName]
						#Add to saved templates in memory
						currentTemplateArray[0]=tabName
						currentTemplateArray[1]=newFrame
						#Create private sections
						sectionCount=0
						for section in sectionList:
							sectionCount+=1
							#Gather Info
							sectionName=section[0]
							viewType=section[1]
							editType=section[2]
							buttonList=section[3]
							hideDataValue=section[5]
							#Create section
							newPrivateSection=privateSection(newFrame)
							newPrivateSection.textVar.set(sectionName)
							newPrivateSection.defaultWidget=viewType
							newPrivateSection.editWidget=editType
							newPrivateSection.loadWidget(viewType)
							newPrivateSection.hideData=hideDataValue
							#Set context to right length
							newPrivateSection.context.setPlaceholders(len(buttonList))
							#Add context buttons to section
							for buttonName in buttonList:
								newPrivateSection.addContextCommand(buttonList.index(buttonName),buttonName)

							#Display on screen
							newPrivateSection.pack(expand=True,fill=BOTH)
							if sectionCount % 2 == 0:
								newPrivateSection.colour("#C3C3C7")
							#Store the section in memory
							currentTemplateArray[2][sectionName]=newPrivateSection
							#Store ref in self dict
							self.sectionDict[sectionName]=newPrivateSection

					#Call the function again to load from memory
					self.loadTemplate(templateName)


			#Update the colour
			templateColour=podTemplate.templateColours[templateName]
			#todo add colour config here

	def addPodData(self,podInstance):
		"""
		This method will take a pod
		and add the data to the notebook
		view.
		"""
		if type(podInstance) is peaPod:
			log.report("Adding pod data")
			#Enable the notebook to insert data
			self.changeNotebookState(False)
			#Clear data first
			self.clearData(allWidgets=True,widgetData=True)
			#Unlock pod if needed
			if podInstance.vaultState:
				podInstance.unlockVault("Unlock")
			#Add the pod data
			for sectionName in self.sectionDict:
				if sectionName in podInstance.vault:
					#Add to screen
					self.sectionDict[sectionName].addData(podInstance.vault[sectionName])

	def clearData(self,**kwargs):
		"""
		Used to clear
		the notebook of all data
		"""
		for section in self.sectionDict:
			self.sectionDict[section].clearData(**kwargs)

	def changeNotebookState(self,chosenState,**kwargs):
		"""
		Will change the state of the notebook
		to either enabled or disabled
		False = Normal
		True = Disabled
		"""
		if self.notebookState == None:
			self.notebookState = not chosenState
		if chosenState == True and self.notebookState == False:
			#Disable the notebook
			for section in self.sectionDict:
				self.sectionDict[section].changeState(chosenState)
			self.notebookState=True
		elif chosenState == False and self.notebookState == True:
			#Enable the notebook
			for section in self.sectionDict:
				self.sectionDict[section].changeState(chosenState)
			self.notebookState=False

	def startEdit(self):
		"""
		Run when the user wants 
		to edit the data on screen
		"""
		#Enable the section
		self.changeNotebookState(False)

		#Load the correct widget
		for sectionName in self.sectionDict:
			sect=self.sectionDict[sectionName]
			#Get old widget data before overwrite
			oldData=sect.getData(stored=True)
			#Load widget
			sect.loadWidget(sect.editWidget)
			#Add the old data
			if oldData:
				sect.addData(oldData)


		#Update the context
		context=None
		context=mainVars.get("context",context)
		if context:
			context.updateContextButton(0, text="Cancel", command=lambda: self.cancelEdit())
			context.updateContextButton(1,text="Save",command=lambda: self.saveEdit())
			context.setPlaceholders(2)

	def cancelEdit(self):
		"""
		Cancel the edit means
		if the user clicks
		 cancel when editing
		 data not saved
		"""
		#Load the correct widget
		for sectionName in self.sectionDict:
			sect=self.sectionDict[sectionName]
			sect.loadWidget(sect.defaultWidget)
			#If the edit and default widgets are same they need to be updated
			if sect.editWidget == sect.defaultWidget:
				sect.restoreData(sect.defaultWidget)

		#Update state of notebook
		self.changeNotebookState(True)

		#Update the context
		context=None
		context=mainVars.get("context",context)
		if context:
			screen.lastScreen.runContext()

	def saveEdit(self):
		"""
		When the user 
		clicks the save button.
		Overwrite the pod data
		"""
		#Overwite
		for sectionName in self.sectionDict:
			sect=self.sectionDict[sectionName]
			#Get the new data
			newData=sect.getData()
			#Get the old data to compare with
			oldData=sect.getData(widget=sect.savedWidgets[sect.defaultWidget],stored=True)
			#Only update if changed
			if newData != oldData:
				#Update the edit widget
				sect.addData(newData)
				#Update stored
				sect.savedWidgetData[sect.defaultWidget]=newData
				#Update current
				sect.addData(newData,widget=sect.defaultWidget)

				#Get the sect name
				currentSectionName=sect.textVar.get()
				#Update the stored data
				currentPeaPod=masterPod.currentMasterPod.currentPeaPod
				currentPeaPod.updateVault(currentSectionName,newData)

		#Save the current master pod
		masterPod.currentMasterPod.save()
		self.cancelEdit()

class selectionBar(mainFrame):
	"""
	The selection bar
	is a bar that allows a single 
	selection. This can be used
	to naivgate etc.
	"""
	def __init__(self,parent,**kwargs):
		mainFrame.__init__(self,parent,**kwargs)

		#Background colour for selection bar
		self.preserveColour=True


		#Colours for tabs
		self.selectedTabColour=mainBlueColour
		self.notSelectedTabColour=mainGreyColour
		self.notSelectedHoverTabColour=mainSecondGreyColour

		#Place for the tabs
		self.centerFrame=mainFrame(self)
		self.centerFrame.pack(expand=True)

		#Store tab data
		self.tabList=[]
		self.currentIndex=None

	def addPlace(self,**kwargs):
		"""
		Will add a placeholder
		for the selection bar
		"""
		places=1
		places=kwargs.get("places",places)
		for x in range(places):
			#Create a button
			newButton=mainButton(self.centerFrame,enabledColour=self.notSelectedTabColour,
			                     hoverColour=self.notSelectedHoverTabColour)
			newButton.pack(fill=BOTH,expand=True,side=LEFT)
			#Store the button
			self.tabList.append(["New Tab",newButton,None])
			#Add the tab
			self.addTab("New Tab",index=len(self.tabList)-1)

	def removePlace(self,index):
		"""
		This method will remove a place 
		in the selection bar
		"""
		if index < len(self.tabList) and index >= 0:
			#Check if it was current
			if index == self.currentIndex:
				self.runTabCommand(0)
			#Remove the button
			button=self.tabList[index][1]
			button.pack_forget()
			#Remove the ref
			del self.tabList[index]

	def addTab(self,tabName,**kwargs):
		"""
		This method will add
		a tab to the selection bar
		if no index specified it will
		add to the end
		"""
		#Default index is last item in list
		tabIndex=len(self.tabList)
		last=False
		command=None
		#Attempt to get index from kwargs
		tabIndex=kwargs.get("index",tabIndex)
		command=kwargs.get("command",command)
		last=kwargs.get("last",last)

		#If last is specified
		if last:
			tabIndex=len(self.tabList)-1

		#Check if index is valid
		if type(tabIndex) is int:
			if tabIndex > len(self.tabList) or tabIndex < 0:
				tabIndex=len(self.tabList)
		else:
			tabIndex=len(self.tabList)

		#Add place if needed
		if tabIndex == len(self.tabList):
			self.addPlace()

		#Update data
		self.tabList[tabIndex][0]=tabName
		self.tabList[tabIndex][2]=command
		butt=self.tabList[tabIndex][1]
		self.updateTab(tabIndex,text=tabName,command=lambda: self.runTabCommand(self.tabList.index([tabName,butt,command])))

		#If index is 0 then run it
		if tabIndex == 0:
			self.runTabCommand(0,forced=True)

	def updateTab(self,index,**kwargs):
		"""
		Used to update the button
		at a specific index 
		"""
		correctButton=self.tabList[index][1]
		correctButton.updateButton(**kwargs)

	def runTabCommand(self,index,**kwargs):
		"""
		This is what is called when the
		tabs button is pressed
		"""
		#Can be forced to run to override
		forced=False
		forced=kwargs.get("forced",forced)
		#Avoid running tab command on current tab
		if index != self.currentIndex or forced == True:
			#Update the old current tab
			if type(self.currentIndex) is int:
				self.updateTab(self.currentIndex,enabledColour=self.notSelectedTabColour,
				               hoverColour=self.notSelectedHoverTabColour)

			#Update the colour
			self.currentIndex=index
			self.updateTab(index,enabledColour=self.selectedTabColour,
			               hoverColour=self.selectedTabColour)

			#Run the command
			commandToRun=self.tabList[index][2]
			if commandToRun:
				runCommand(commandToRun,name="Running selection bar tab command")

	def setSize(self,numberOfPlaces):
		"""
		Will set the bar to the set number
		of places
		"""
		#Get the number of tabs
		numberOfTabs=len(self.tabList)

		#It tabs need to be created
		if numberOfPlaces > numberOfTabs:
			#Calculate number of places needed
			numberNeeded=numberOfPlaces-numberOfTabs
			self.addPlace(places=numberNeeded)

		#If tabs need to be removed
		elif numberOfPlaces < numberOfTabs and numberOfPlaces >= 1:
			#Calculate slicing
			numberToRemove=numberOfTabs-numberOfPlaces
			counter=0
			for x in range(numberOfPlaces,len(self.tabList)):
				self.removePlace(x-counter)
				counter+=1

class advancedSlider(mainFrame):
	"""
	This class is a modified scale widget.
	It will add more customization and 
	a label kwarg which adds a label to the widget
	"""


	def __init__(self,parent,text,*extra,**kwargs):

		mainFrame.__init__(self,parent)

		#Important
		self.text=text
		self.outputVar=StringVar()
		self.commands=[]

		#UI
		self.label=mainLabel(self,text=self.text)
		self.label.pack()

		self.sliderContainer=mainFrame(self)
		self.sliderContainer.pack()

		self.slider=ttk.Scale(self.sliderContainer,length=150,**kwargs)
		self.slider.grid(row=0,column=0)

		self.outputLabel=mainLabel(self.sliderContainer,textvariable=self.outputVar,width=5)
		self.outputLabel.grid(row=0,column=1)

		#Update label
		self.outputVar.set(self.getValue())

		#Adds command run
		self.slider.config(command=lambda event: self.run(event))

	def addCommand(self,command):
		"""
		Will add a command to the list to execute
		when slider moves
		"""
		if command not in self.commands:
			self.commands.append(command)

	def run(self,value):
		"""
		This is the method called every time the slider
		moves
		"""
		value=int(float(value))

		#Run the commands
		for command in self.commands:
			try:
				command()
			except:
				log.report("Error running command","(Slider)",tag="Error",system=True)
		#Update label
		self.outputVar.set(value)

	def getValue(self):
		return int(float(self.slider.get()))

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
	#Store a reference
	templates={}
	#Store valid data types
	validDataTypes=[Entry,advancedEntry,Text,advancedOptionMenu,Label,mainLabel]

	def __init__(self,templateName,templateColour):
		#Name and Colour of template
		self.templateName=templateName
		self.templateColour=templateColour
		#Store the tabs
		self.tabs={}
		#Stores the tab names in their order
		self.tabOrder=[]
		#Add to class dict for reference
		podTemplate.templateColours[self.templateName]=self.templateColour
		podTemplate.templates[self.templateName]=self

	def addTab(self,tabName):
		"""
		This method allows a tab to be
		easily added to the template which is
		an area to store data.
		"""
		#Initiate an empty dictionary in the tab dictionary
		self.tabs[tabName]=[]
		self.tabOrder.append(tabName)

	def addTemplateSection(self,tabName,sectionName,viewType,editType,buttonList,**kwargs):
		"""
		This method allows a section of data to be added to the template.
		For example a section for "Password" or "Email" 
		"""
		if tabName in self.tabs:
			#Get section colour
			sectionColour="#FFFFFF"
			sectionColour=kwargs.get("colour",sectionColour)
			#Should the data be hidden when possible
			hideData=False
			hideData=kwargs.get("hide",hideData)
			#Add the data to list
			dataArray=[sectionName,viewType,editType,buttonList,sectionColour,hideData]
			#Add list to dictionary
			self.tabs[tabName].append(dataArray)


#====================Create the pod templates====================


#=====Login======
loginTemplate=podTemplate("Login","#A9F955")
loginTemplate.addTab("Login")
loginTemplate.addTemplateSection("Login","Username",mainLabel,Entry,["Copy","Hide"])
loginTemplate.addTemplateSection("Login","Password",mainLabel,Entry,["Copy","Hide"],hide=True)

loginTemplate.addTab("Advanced")
loginTemplate.addTemplateSection("Advanced","Website",mainLabel,Entry,["Copy","Hide","Launch"])
loginTemplate.addTemplateSection("Advanced","Notes",Text,Text,["Copy"])

#=====Secure Note======
secureNoteTemplate=podTemplate("SecureNote","#78C2D2")
secureNoteTemplate.addTab("Note")
secureNoteTemplate.addTemplateSection("Note","Note",Text,Text,["Copy"])

#=====Card======
cardTemplate=podTemplate("Credit Card","#EE658A")
cardTemplate.addTab("Card")
cardTemplate.addTemplateSection("Card","Card Holder Name",mainLabel,Entry,["Copy","Hide"])
cardTemplate.addTemplateSection("Card","Bank",mainLabel,Entry,["Copy","Hide"])
cardTemplate.addTemplateSection("Card","Card Number",mainLabel,Entry,["Copy","Hide"],hide=True)
cardTemplate.addTemplateSection("Card","Expire date",mainLabel,Entry,["Copy","Hide"])
cardTemplate.addTab("Advanced")
cardTemplate.addTemplateSection("Advanced","Pin",mainLabel,Entry,["Copy","Hide"],hide=True)
cardTemplate.addTemplateSection("Advanced","Credit limit",mainLabel,Entry,["Copy","Hide"])
cardTemplate.addTemplateSection("Advanced","Notes",Text,Text,["Copy"])
#=====Password======
passwordTemplate=podTemplate("Password","#E6BE3E")
passwordTemplate.addTab("Password")
passwordTemplate.addTemplateSection("Password","Password",mainLabel,Entry,["Copy","Hide"],hide=True)
passwordTemplate.addTemplateSection("Password","Notes",Text,Text,["Copy"])





