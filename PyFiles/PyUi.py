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

#====================Secondary Classes====================
"""
Secondary classes are classes that inherit from the core classes
and are more program specific.
"""

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

