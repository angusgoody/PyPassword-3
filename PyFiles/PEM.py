# coding=utf-8

#Angus Goody
#12/10/17
#PyPassword 3 Pod Encryption Module

"""
This file is the encryption module
and all decrypting and encrypting of 
data takes place here.
"""

#====================Imports====================
import pickle
from datetime import datetime
import os
from random import choice
from tkinter import PhotoImage,messagebox
#====================Variables====================
dataDirectory="PyData"
logDirectory="PyLogs"
filesDirectory="PyFiles"
assetDirectory="PyAssets"
#====================Arrays====================
masterPodColours=["#0DE5D5","#81AFBA","#2E467B","#06486F","#CBF8FC"]
#====================Log====================
class logClass:
	"""
	The logClass is a way of recording
	events that go on throughout 
	the program. Each file has its own
	logClass which it reports to during runtime
	"""
	logs={}
	def __init__(self,logName):
		self.logName=logName
		#Add the logClass to all logs
		logClass.logs[logName]=self
		#Store the data
		self.systemData={}
		self.generalData={}
		#Store tags
		self.tags={}

	def report(self,message,*extra,**kwargs):
		"""
		The report method reports
		 a problem or event to the 
		 logClass.
		"""
		#Variables
		dataDictionary=self.generalData
		tag="Default"

		#Create message string
		if len(extra) > 0:
			for item in extra:
				message+=" "
				message+=str(item)


		#Check for tags
		if "tag" in kwargs:
			tag=kwargs["tag"]

		#Check for system or default data
		if "system" in kwargs:
			if kwargs["system"]:
				dataDictionary=self.systemData

		#Get current time
		currentTime=datetime.now().strftime('%Y-%m-%d %H:%M:%S')

		#Report to class
		dataDictionary[currentTime]=message

	def saveLog(self):
		"""
		This method will save the logClass
		to file using pickle. It can then
		viewed and loaded in PyPassword, 
		error and default data will only be saved
		to file to save space.
		"""
		#Create the file name
		fileName=self.logName+"Log.log"

		fileName=getLocalFileName(fileName,"Logs")

		#Open the file
		file=open(fileName,"a")

		#Save the default data
		for item in self.generalData:
			writeString=str(self.generalData[item])
			writeString+=","
			writeString+=item
			writeString+=",Default\n"
			file.write(writeString)

		#Close file
		file.close()

#Initiate PEM logClass
log=logClass("Encryption")

#====================Functions====================
"""
These functions are used for generating passwords, 
and also encrypting and decrypting data.
"""

#Utility functions



def runCommand(command,**kwargs):
	"""
	This function will safley run
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
	except:
		log.report("Error executing command through function",identifier,tag="Error")
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
#Folder and Directory functions
def getWorkingDirectory():
	"""
	Will return the current working directory the program is in
	"""
	currentDirectory=os.path.dirname(os.getcwd())
	return currentDirectory

def getLocalFileName(baseFileName,indicator):
	"""
	This function will return a string used
	for saving files in the new PyPassword
	file structure, it will get the current
	directory and the subfolder and add the file
	name so files are saved in the correct place
	"""
	#Setup variable for file name
	wholeFileName=""

	#Get the working directory
	currentDirectory=getWorkingDirectory()

	#Find correct sub folder to match parameter
	subFolder=""
	if indicator.upper() == "FILES":
		subFolder=filesDirectory
	elif indicator.upper() == "LOGS":
		subFolder=logDirectory
	elif indicator.upper() == "ASSETS":
		subFolder=assetDirectory
	else:
		subFolder=dataDirectory

	#Add subFolder to base directory
	wholeFileName=currentDirectory+"/"+subFolder

	#If the directory does not exist create it
	if not os.path.isdir(wholeFileName):
		os.makedirs(wholeFileName)

	#Add base file to file name
	wholeFileName=wholeFileName+"/"+str(baseFileName)

	#Return
	return wholeFileName

def checkLocation(fileName):
	"""
	This function will check a file name
	to see if the directory exists
	and if a file can be saved there
	"""
	if fileName:
		directory=os.path.dirname(fileName)
		if not os.path.isdir(directory):
			log.report("Invalid directory detected",fileName)
			return False
		else:
			return True
	else:
		return False

def findFiles(directory,extension):
	"""
	This function searches through
	a directory to look for a certain 
	file type and return an array with
	the files
	"""
	filesFound=[]
	for root, dirs, files in os.walk(directory, topdown=False):
		for name in files:
			fileFound=(os.path.join(root, name))
			base=os.path.basename(fileFound)
			if base.endswith(extension):
				filesFound.append(fileFound)

	return filesFound

def getRootName(directory):
	#Get the root file name of directory
	return os.path.splitext(os.path.basename(directory))[0]

def getPicture(pictureName):
	"""
	This function will attempt to find 
	a picture in the PyAssets directory and 
	return the result as a photoImage.
	"""
	#Get full name
	fullName=getLocalFileName(pictureName,"Assets")
	#Check file exists
	if (os.path.exists(fullName)):
		photo=PhotoImage(file=fullName)
	else:
		photo=PhotoImage(file="")

	return photo

#Pickle Functions
def openPickle(fileName):
	"""
	This function opens a pickle file
	and returns the content
	"""
	try:
		content=pickle.load( open( fileName, "rb" ) )
	except:
		log.report("Error reading file when pickling")
		return None
	else:
		return content

def savePickle(content,fileName):
	"""
	This function will dump
	a pickle file to a directory
	"""
	pickle.dump(content, open( fileName, "wb" ) )
	log.report("Save complete exported to", fileName, tag="File")

#Encryption functions
def encrypt(plainText,key):
	"""
	The encrypt function will
	take the inputs of plain text,
	encrypt it using the key and 
	return the result
	"""

def decrypt(plainText,key):
	"""
	The decrypt function will
	take the inputs of plain text,
	decrypt it using the key and 
	return the result
	"""
	pass

#====================Core Classes====================
"""
The PEM core classes are the classes that form the basic 
structure of PyPasswords security, they are the classes
the sensitive data is stored in.
"""

class peaPod:
	"""
	The peaPod class is a class
	for each account stored in PyPasssword.
	It will securely store data using
	encryption
	"""
	def __init__(self,master,peaName):
		#Store the parent master peaPod
		self.master=master
		#Name of the peaPod
		self.peaName=peaName
		#Encrypted vault where info is stored
		self.vault={}
		#Store template type
		self.templateType="Login"
		#Store Vault state
		self.vaultState="Unlocked"

	def unlockVault(self,unlockOrLock):
		"""
		This method will secure the vault
		and encrypt or decrypt the vault 
		depending on the parameter passed
		to the function.
		"""
		#Check the vault is in the correct state
		valid=False
		if unlockOrLock == "Lock":
			if self.vaultState == "Unlocked":
				valid=True
		else:
			if self.vaultState == "Locked":
				valid=True

		if valid:
			#Get the key to encrypt with
			encryptionKey=self.master.masterKey
			#Iterate through peaPod
			for item in self.vault:

				#Encrypt data
				if unlockOrLock == "Lock":
					secureName=encrypt(item,encryptionKey)
					secureData=encrypt(self.vault[item],encryptionKey)

				#Decrypt data
				else:
					secureName=decrypt(item,encryptionKey)
					secureData=decrypt(self.vault[item],encryptionKey)

				#Add to the vault
				self.vault[secureName]=secureData
				#Remove old data
				del (self.vault,item)

			log.report(unlockOrLock,"peaPod vault",self.peaName)
		else:
			log.report("Attempted to encrypt locked vault")

class masterPod:
	"""
	The master peaPod class is the class
	which stores all the smaller data
	for every account stored in PyPassword
	"""
	currentMasterPod=None
	loadedPods={}
	def __init__(self,name):
		#Name of the master peaPod
		self.masterName=name
		self.masterColour=choice(masterPodColours)
		self.baseName=self.masterName+".mp"
		#Store the key
		self.key=None
		#Where the pods are stored
		self.peas={}
		#The master key used for encryption
		self.masterKey=None
		#Where the master peaPod is saved
		self.location=None
		#Add to loaded pods
		masterPod.loadedPods[self.masterName]=self

	def save(self):
		"""
		This method saves the master peaPod to file
		and ensures all the data is encrypted and
		secure, it also allows .mp files
		to be opened from other locations and then
		auto saved in the correct place if the directory
		is invalid
		"""
		#Ensure all pods are secure
		for pod in self.peas:
			if pod.vaultState != "Locked":
				pod.unlockVault("Lock")

		#First check location is valid
		if checkLocation(self.location) is False:
			#If not create a new file in the correct place
			fileName=getLocalFileName(self.baseName,"Data")
			self.location=fileName
		else:
			fileName=self.location

		#Save self to pickle
		savePickle(self,fileName)

#====================Core Functions====================

def loadMasterPodFromFile(fileName):
	"""
	Load a master pod from directory
	and create a class instance 
	"""
	#De Pickle the file
	contents=openPickle(fileName)
	if contents:
		if type(contents) == masterPod:
			#Add to loaded pods dictionary
			masterPod.loadedPods[contents.masterName]=contents
			#Return the master pod
			return contents


#====================Testing area====================

