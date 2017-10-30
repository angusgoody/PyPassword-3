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

def recursiveColour(parent,colour,**kwargs):
	"""
	The recursive colour function
	will change the colour of widgets
	recursively
	"""
	#Items to exclude
	excludeItems=[]

	#Items who's highlight background is changed
	highlightItems=["Entry", "Button", "Text", "Listbox", "OptionMenu", "Menu"]

	#Check to see if any widgets should be excluded
	if "exclude" in kwargs:
		#Add new items to exclude
		excludeItems.extend(kwargs["exclude"])

	#Check if parent has children
	if "winfo_children" in dir(parent):
		pass
	else:
		pass
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
		pass

	def addBinding(self,bindButton,bindFunction):
		"""
		This method will allow the widget
		to be binded to a function recursively meaning
		all the children are also binded.
		"""
		pass

class mainButton(mainFrame):
	"""
	The main Button class
	if a custom button class
	that handles bindings and colours
	etc
	"""
	def __init__(self,parent,**kwargs):
		mainFrame.__init__(self,parent)
		#Store the command
		self.command=None
		#Store button state
		self.state=True
		self.hoverState=False
		#Button colour variables
		self.hoverColour="#61D9CD"
		self.clickedColour="#60EFD0"
		self.disabledColour="#ACB4B4"
		self.enabledColour="#EEF6F5"
		#Text frame
		self.textFrame=mainFrame(self)
		self.textFrame.pack(expand=True)
		#Text
		self.textVar=StringVar()
		self.textLabel=Label(self.textFrame)
		#Bindings
		recursiveBind(self,"<Enter>",)

	def runCommand(self):
		"""
		This method will execute the command
		stored inside the button
		"""
		#Check the button has a command
		if self.command:
			try:
				self.command()
			except:
				log.report("Error executing button command",tag="Error")

	def hover(self):
		"""
		This method is run when the mouse
		hovers over the button, depending
		on the state of the button it will change 
		colour
		"""
		if self.state:
			#If the hover state is false then hover is not active
			if self.hoverState == False:
				#Activate hover
				self.hoverState=True
				#Change colour




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
		self.buttonArray.append("")



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

