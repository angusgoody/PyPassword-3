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
from PEM import logClass

#====================Log====================

log=logClass("User Interface")
log.saveLog()
#====================Preset variables====================

#====================LOG====================

class log:
	"""
	The Log class stores logged
	events in the program, errors
	etc.
	"""
	def __init__(self,logName):
		self.logName=logName
		self.logData={}
		self.systemData={}

#====================Functions====================
"""
This section is for functions that aid with the user
interface elements of PyPassword
"""

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
	excludeItems=[]

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
		self.state=False
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
		self.textLabel=Label(self,textvariable=self.textVar,width=self.labelWidth,font=self.font)
		self.textLabel.pack(expand=True)
		#Bindings
		self.addBinding("<Enter>",lambda event: self.hover(True))
		self.addBinding("<Leave>",lambda event: self.hover(False))
		self.addBinding("<Button-1>",lambda event: self.runCommand())
		self.addBinding("<ButtonRelease-1>",lambda event: self.pressBind(False))

		#Check for Kwargs
		self.updateButton(**kwargs)

		#Initiate Button state
		self.changeState(True)

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

		#Update the widgets etc
		self.textLabel.config(font=self.font)
		self.textLabel.config(textvariable=self.textVar)
		#Only update colour if mouse is not over button
		if self.state == True and self.hoverOn == False and self.pressing == False:
			self.changeButtonColour(self.enabledColour)

	def changeButtonColour(self,bg,**kwargs):
		"""
		This method is used to change the buttons colour
		and change its background and text colour if needed
		temporarily only
		"""
		#Change the colours with overide True
		self.colour(bg,overide=True)
		self.textLabel.config(fg=getColourForBackground(bg))

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

			#Run the command
			try:
				self.command()
			except:
				log.report("Error executing button command",tag="Error")

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
		#Store text data
		self.textVar=StringVar()
		self.textVar.set("Label")
		#Store look of the label
		self.fg=None
		self.colour="#FFFFFF"
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
		self.colour=kwargs.get("colour",self.colour)

		#Update
		self.config(textvariable=self.textVar)
		if self.fg == None:
			self.config(fg=getColourForBackground(self.colour),font=self.font)
		else:
			self.config(fg=self.fg)





#====================Secondary Classes====================
"""
Secondary classes are classes that inherit from the core classes
and are more program specific.
"""

class screen(mainFrame):
	"""
	The screenclass is a class
	for every screen in PyPassword.
	It is a frame that can be hidden and shown
	"""
	lastScreen=None
	statusVar=None
	def __init__(self,parent,screenName,**kwargs):
		mainFrame.__init__(self,parent)
		self.screenName=screenName
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
			if "set" in dir(screen.statusVar):
				screen.statusVar.set(self.screenName)
				print(self.screenName)
			#Set as last screen
			screen.lastScreen=self

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
		self.defaultText="Comand"
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
		self.updateBar(**kwargs)

	def updateBar(self,**kwargs):
		"""
		Update the bar with KWARGS
		"""
		#Get kwargs
		self.font=kwargs.get("font",self.font)
		#Update
		for button in self.buttonArray:
			button.updateButton(font=self.font)

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

	def addButton(self,index,**kwargs):
		"""
		This method allows a button to be added
		to the context bar
		"""
		if index+1 <= len(self.buttonArray) and index >= 0:
			self.buttonArray[index].updateButton(**kwargs)

class multiView(mainFrame):
	"""
	The multi view is a class
	which allows multiple frames
	to be displayed in one place
	and swapped around.
	"""
	def __init__(self,parent):
		mainFrame.__init__(self,parent)
		#Store the view info
		self.views={}
		self.currentView=None

	def addView(self,frameToDisplay,name):
		"""
		This method will allow a frame
		to be added to the multi view 
		"""
		self.views[name]=frameToDisplay

	def showView(self,frameName):
		"""
		This method will load a frame
		to dislpay on the multiview
		"""
		#Check valid parameter
		if frameName in self.views:
			pass

