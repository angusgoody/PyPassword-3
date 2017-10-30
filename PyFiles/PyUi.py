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
	def __init__(self,parent):
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
		#Button colour variables
		self.hoverColour="#E852F3"
		self.clickedColour="#60EFD0"
		self.disabledColour="#ACB4B4"
		self.disabledFG="#939797"
		self.enabledColour="#2CF3C7"
		self.enabledFG="#000000"
		#Text
		self.textVar=StringVar()
		self.textVar.set("Button")
		self.textLabel=Label(self,textvariable=self.textVar,width=12)
		self.textLabel.pack(expand=True)
		#Bindings
		self.addBinding("<Enter>",lambda event: self.hover(True))
		self.addBinding("<Leave>",lambda event: self.hover(False))
		self.addBinding("<Button-1>",lambda event: self.runCommand())

		#Initiate Button state
		self.changeState(True)


	def runCommand(self):
		"""
		This method will execute the command
		stored inside the button
		"""
		#Check the button has a command
		if self.command and self.state:
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
				#Activate hover
				self.hoverOn=True
				#Change colour#
				self.colour(self.hoverColour,overide=True)
			else:
				#Deactivate hover
				self.hoverOn=False
				#Change colours
				self.colour(self.enabledColour,overide=True)

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
			self.colour(self.enabledColour,overide=True)
			self.textLabel.config(fg=self.enabledFG)
		#Turn off
		elif TrueOrFalse == False and self.state:
			self.state=False
			#Change colours
			self.colour(self.disabledColour,overide=True)
			self.textLabel.config(fg=self.disabledFG)




#====================Secondary Classes====================
"""
Secondary classes are classes that inherit from the core classes
and are more program specific.
"""
class contextBar(mainFrame):
	"""
	The contextBar class will be a class
	that stretches across the screen and has
	contextual buttons to execute. That can
	be swapped and modified to suit onscreen
	actions
	"""
	def __init__(self,parent):
		mainFrame.__init__(self,parent)

		#Store name and command in dictionary
		self.nameDict={}
		#The array that stores buttons
		self.buttonArray=[]
		#Store number of active sections
		self.sections=0
		#Section Types
		self.sectionTypes=["Button","Checkbutton"]

	def addPlaceholder(self):
		"""
		This method will add a section to 
		the context bar which can be used
		to add a button
		"""
		self.sections+=1
		self.buttonArray.append(mainButton(self))



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

