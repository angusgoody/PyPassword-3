# coding=utf-8


#Imports
import threading
from tkinter import *
import time
from PEM import *

class threadController:
	"""
	The thread controller class
	controls the threads for a whole
	program and ensures they run smoothly
	"""
	def __init__(self):
		#Store the commands
		self.threadCommands={}
		#Store if the thread is running currently or not
		self.threadLocks={}
		#Store the thread objects
		self.threadObjects={}

	def createThread(self,threadName,command):
		"""
		Initiate a thread and store the info about
		the thread.
		"""
		#Store the thread value
		self.threadCommands[threadName]=command
		self.threadLocks[threadName]=False

	def runThread(self,threadName,**kwargs):
		"""
		Run a thread and start the process
		"""
		if threadName in self.threadLocks and threadName in self.threadCommands:
			#First check if running
			if self.threadLocks[threadName] is True:
				print("Thread in progress")
				#Check if thread object has ended
				if threadName in self.threadObjects:
					if self.threadObjects[threadName].isAlive() is not True:
						self.threadLocks[threadName]=False
						print("Thread has actually ended now")
						#Call function again to create new thread
						self.runThread(threadName)

			else:
				#Create and run the thread and store value as True
				newThread=threading.Thread(target=self.threadCommands[threadName],kwargs=kwargs)
				#Ensure the thread can be killed when program ends
				newThread.daemon=True
				self.threadLocks[threadName]=True
				self.threadObjects[threadName]=newThread
				newThread.start()
				print("New thread started")


def startTimer():
	"""
	Function to start
	the countdown timer
	"""
	timerAmount=1
	#Calc future time
	futureTime=addTimeToCurrent("minutes",timerAmount)
	currentTime=getCurrentTime()
	while futureTime > currentTime:
		currentTime=getCurrentTime()
		if currentTime < futureTime:
			timeRemaining=calculateTimeRemaining(futureTime,currentTime,"string")
			mainLabelVar.set(timeRemaining)
			time.sleep(0.2)
		else:
			mainLabelVar.set("Timer complete!")


def startNewTimer(minutes):
	futureTime
root=Tk()
root.geometry("400x300")
root.title("Countdown")

centerFrame=Frame(root)
centerFrame.pack(expand=True)

#Main Label
mainLabelVar=StringVar()
mainLabelVar.set("5:00")
mainLabel=Label(centerFrame,textvariable=mainLabelVar,font="Avenir 23")
mainLabel.pack()

#Start button
startButton=Button(centerFrame,text="Start timer",command=lambda: mainThread.runThread("runCountdown"))
startButton.pack(pady=5)

#Setup thread
mainThread=threadController()
mainThread.createThread("runCountdown",startTimer)

#End the program loop
root.mainloop()