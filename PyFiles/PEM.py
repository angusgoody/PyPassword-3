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
from datetime import datetime,timedelta
import os
from random import choice
from tkinter import PhotoImage,messagebox
from Crypto.Cipher import AES

#====================Variables====================
dataDirectory="PyData"
logDirectory="PyLogs"
filesDirectory="PyFiles"
assetDirectory="PyAssets"

lockedMinutes=5
#====================Arrays====================
masterPodColours=["#0DE5D5","#81AFBA","#2E467B","#06486F","#CBF8FC"]
masterPodAttempts={}
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
		tag=kwargs.get("tag",tag)

		#Check for system or default data
		if "system" in kwargs:
			if kwargs["system"]:
				dataDictionary=self.systemData

		#Get current time
		currentTime=datetime.now().strftime('%Y-%m-%d %H:%M:%S')

		#Report to class
		dataDictionary[currentTime]=[message,tag]

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
			writeString=str(self.generalData[item][0])
			writeString+=","
			writeString+=item
			writeString+=","
			writeString+=str(self.generalData[item][1])
			writeString+="\n"
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
def pad(text):
	"""
	For AES encryption keys and data must
	be in multiples of 16 so the pad function
	adds padding to make it the right length
	"""
	return text +((16-len(text) % 16)*"\n")

def encrypt(plainText, key):
	"""
	This is the encrypt function 
	which will encrypt plain text
	using AES encryption
	"""
	if plainText:
		#Pad the key to ensure its multiple of 16
		key=AES.new(pad(key))
		#Pad the plain text to ensure multiple of 16
		text=pad(str(plainText))
		#Encrypt using module
		encrypted=key.encrypt(text)
		return encrypted
	else:
		return plainText

def decrypt(data, key):
	"""
	The decrypt function
	will decrypt any plain text 
	data and return the result.
	"""
	try:
		#Pad the key
		key=AES.new(pad(key))
		#Use module to decrypt data
		data=key.decrypt(data).rstrip()
		#Report
		log.report("Data decrypted")
		try:
			data=data.decode("utf-8")
		except:
			return None
		else:
			return data
	except:
		log.report("An error occurred when attempting to decrypt","(Decrypt)",tag="Error")
		return None

#Time functions
def getCurrentTime():
	return datetime.now()

def addTimeToCurrent(unit,value):
	"""
	Get the current system time
	and add a value onto this
	"""
	currentTime=getCurrentTime()
	if unit == "minutes":
		newTime=currentTime+timedelta(minutes=value)
	elif unit == "seconds":
		newTime=currentTime+timedelta(seconds=value)
	else:
		newTime=getCurrentTime()
	return newTime

def calculateTimeRemaining(time1,time2,stringOrRaw):
	"""
	Calculate the difference between two
	times. StringOrRaw specifies whether
	the object or string should be returned
	Time1 = Bigger
	string=string
	raw=raw
	"""
	#Calculate time remaining
	timeRemaining=(time1-time2)
	if stringOrRaw == "raw":
		return timeRemaining
	else:
		timeList=str(timeRemaining).split(":")
		hours=timeList[0]
		minutes=timeList[1]
		seconds=timeList[2].split(".")[0]
		timeRemainingString=hours+":"+minutes+":"+seconds
		return timeRemainingString

#====================Core Classes====================
"""
The PEM core classes are the classes that form the basic 
structure of PyPasswords security, they are the classes
the sensitive data is stored in.
"""

class keyBox:
	"""
	The key box
	is a place to store
	encryption keys while the program
	is running. It will clear
	when the program is killed.
	"""
	keyHoles={}
	def __init__(self,masterPodInstance,key):
		self.masterPodInstance=masterPodInstance
		self.key=key
		#Add to dict
		keyBox.keyHoles[masterPodInstance]=self

class peaPod:
	"""
	The peaPod class is a class
	for each account stored in PyPasssword.
	It will securely store data using
	encryption
	
	Vault state
	True = Unlocked
	False = Locked
	"""
	
	def __init__(self,master,peaName,**kwargs):
		#Store the parent master peaPod
		self.master=master
		#Name of the peaPod
		self.peaName=peaName
		#Encrypted vault where info is stored
		self.vault={}
		#Store template type
		self.templateType="Login"
		#Store Vault state True = Locked False = Unlocked
		self.vaultState=False

		#Update
		self.update(**kwargs)

	def update(self,**kwargs):
		"""
		The update method for peaPod.
		"""
		self.templateType=kwargs.get("template",self.templateType)

	def updateVault(self,sectionName,data):
		"""
		This method allows new data
		to be stored in the peaPod. 
		"""
		#If title is updated
		if sectionName == "Title":
			self.peaName=data
		#Ensure pod vault is unlocked
		self.unlockVault("Unlock")
		if sectionName in self.vault:
			log.report("Vault updated with new info",self.peaName)
			self.vault[sectionName]=data
		elif sectionName not in self.vault:
			log.report("New section added to the vault",self.peaName)
			self.vault[sectionName]=data

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
			if self.vaultState == False:
				valid=True
		else:
			if self.vaultState == True:
				valid=True

		if valid:
			#Get the key to encrypt with
			encryptionKey=self.master.getKey()
			#Iterate through peaPod
			newVault={}
			for item in self.vault:

				#Encrypt data
				if unlockOrLock == "Lock":
					secureName=encrypt(item,encryptionKey)
					secureData=encrypt(self.vault[item],encryptionKey)

				#Decrypt data
				else:
					secureName=decrypt(item,encryptionKey)
					secureData=decrypt(self.vault[item],encryptionKey)

				#Add to the new vault
				newVault[secureName]=secureData

			#Update the vault to the new secure vault
			self.vault=dict(newVault)
			#Update the variable
			if unlockOrLock == "Lock":
				self.vaultState=True
			else:
				self.vaultState=False
			log.report(unlockOrLock,"peaPod vault",self.peaName)
		else:
			log.report("Attempted to encrypt locked vault")

	def addSensitiveData(self,dataName,data):
		"""
		This is where the data is added
		to the pea. the data name refers
		to what the data is "Password" etc and
		the data is the actual password
		"""
		if self.vaultState == False:
			self.vault[dataName]=data
		else:
			log.report("Could not save data to pod because currently locked")

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
		#Key used for checking master key
		self.checkKey="key"
		#Store the hint
		self.hint="No Hint Available"
		#Where the pods are stored
		self.peas={}
		#Store currently loaded pea pod
		self.currentPeaPod=None
		#Where the master peaPod is saved
		self.location=None
		#Add to loaded pods
		masterPod.loadedPods[self.masterName]=self

		#Locked info
		self.locked=getCurrentTime()

	def save(self):
		"""
		This method saves the master peaPod to file
		and ensures all the data is encrypted and
		secure, it also allows .mp files
		to be opened from other locations and then
		auto saved in the correct place if the directory
		is invalid
		"""
		#Close the pod (Encrypt etc)
		self.close()
		print("Closing complete")
		#First check location is valid
		if checkLocation(self.location) is False:
			#If not create a new file in the correct place
			fileName=getLocalFileName(self.baseName,"Data")
			self.location=fileName
		else:
			fileName=self.location

		#Save self to pickle
		savePickle(self,fileName)

	def addPeaPod(self,podName,**kwargs):
		"""
		This method allows a pea
		to be saved to the master pod.
		"""
		#Create a new pod
		newPod=peaPod(self,podName,**kwargs)
		#Add to the dictionary
		self.peas[podName]=newPod
		#Return the peaPod
		return newPod

	def addPeaPodData(self,peaPodName,dataName,data):
		"""
		This method allows sensitive information
		to be added to a peaPod.
		"""
		#Check pea exists
		if peaPodName in self.peas:
			#Get the peaPod
			peaInstance=self.peas[peaPodName]
			#Add the data to vault
			peaInstance.addSensitiveData(dataName,data)

	def close(self):
		"""
		This function will close the master pod
		and secure the data
		"""
		#Ensure all pods are secure
		for podName in self.peas:
			pod=self.peas[podName]
			if pod.vaultState == False:
				pod.unlockVault("Lock")

		#Encrypt the key to a vaule which can only be decrypted with current key
		encryptionKey=self.getKey()
		if encryptionKey:
			self.checkKey=encrypt("key",encryptionKey)
		else:
			log.report("Could not find encryption key")

	def getKey(self):
		"""
		Will attempt to retrieve
		the encryption key
		from the keybox
		"""
		if self in keyBox.keyHoles:
			key=keyBox.keyHoles[self].key
			return key
		else:
			log.report("Unable to find masterpod key")

	def addKey(self,key):
		"""
		Used to add a encryption key
		to the master pod
		"""
		#Create a keyBox
		newBox=keyBox(self,key)
		log.report("A new master pod encryption key was added for",self.masterName)
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

def checkMasterPodPassword(masterPodInstance, attempt):
	"""
	This is the function in which
	the password is actually decrypted
	and will return a value based on if
	the attempt is correct or not
	"""
	if type(masterPodInstance) is masterPod and hasattr(masterPodInstance,"checkKey"):
		decryptResult=decrypt(masterPodInstance.checkKey,attempt)
		if decryptResult:
			return decryptResult
		else:
			return None
	else:
		log.report("Non master pod passed to function or checkKey is invalid")

def checkMasterPodAttempt(masterPodInstance,attempt):
	"""
	This is the function in which
	the password is actually decrypted
	and will return a value based on if
	the attempt is correct or not
	"""
	if type(masterPodInstance) == masterPod:
		#Check for locked values
		if hasattr(masterPodInstance,"locked"):
			#If the value has been altered then lock the pod
			if type(masterPodInstance.locked) is not datetime:
				log.report("Locked attribute has been changed")
				masterPodInstance.locked=addTimeToCurrent("minutes",lockedMinutes)

			if masterPodInstance.locked < getCurrentTime():
				currentNumberOfAttempts=0
				#Check for a stored number of attempts
				if masterPodInstance in masterPodAttempts:
					currentNumberOfAttempts=masterPodAttempts[masterPodInstance]
				#Create a new dictionary key
				else:
					masterPodAttempts[masterPodInstance]=0

				#Attempt to unlock with password
				decryptResult=checkMasterPodPassword(masterPodInstance,attempt)

				#If the password correct
				if decryptResult:
					masterPodAttempts[masterPodInstance]=0
					#Store the key in a secure key box
					newKey=keyBox(masterPodInstance,attempt)
					return True

				#If the attempt is incorrect
				else:
					#Add one to counter
					currentNumberOfAttempts+=1
					masterPodAttempts[masterPodInstance]=currentNumberOfAttempts
					#Check if limit reached
					if currentNumberOfAttempts == 5:
						masterPodInstance.locked=addTimeToCurrent("minutes",lockedMinutes)
						masterPodAttempts[masterPodInstance]=0
						masterPodInstance.save()
						log.report("Pod locked for 5 minutes",masterPodInstance.masterName)
						return "locked"




			else:
				return "locked"

		#If class does not support locking then add the attribute
		else:
			masterPodInstance.locked=getCurrentTime()
			checkMasterPodPassword(masterPodInstance,attempt)

def createNewPeaPod(masterPodInstance,peaName,template):
	"""
	This function will allow a
	new pea pod to be created
	"""
	pass

#====================Testing area====================

"""
pods=["Amazon","Google","Spotify","Souncloud","PyCharm","Wix","Argos","King Edwards"]


names={"Simon":"Angy","Sam":"gay","Bob":"Bob"}


hints=["A secret hint","Ahahhah me","Never guess me password"]
for item in names:
	newPod=masterPod(item)
	newPod.addKey(names[item])
	newPod.hint=hints.pop()

	podName=pods.pop()
	newPod.addPeaPod(podName)

	newPod.addPeaPodData(podName,"Password","Secret")
	newPod.save()


#""

newMasterPod=masterPod("NewBoi")
newMasterPod.addKey("boi123")
newMasterPod.hint="Boi with 123"

newMasterPod.addPeaPod("my notes",template="SecureNote")
newMasterPod.addPeaPodData("my notes","Title","My note")
newMasterPod.addPeaPodData("my notes","Note","The content of my note")

newMasterPod.addPeaPod("Github")
newMasterPod.addPeaPodData("Github","Username","Angusgoody")
newMasterPod.addPeaPodData("Github","Password","angy123")
newMasterPod.addPeaPodData("Github","Website","github.com")

newMasterPod.save()


newMaster=masterPod("Frank")
newMaster.addKey("frankBoi")
newMaster.hint="Frankly"

newMaster.addPeaPod("Nationwide",template="Credit Card")
newMaster.addPeaPodData("Nationwide","Card Holder Name","Frank")
newMaster.addPeaPodData("Nationwide","Pin","12345")

newMaster.addPeaPod("Vault",template="Password")
newMaster.addPeaPodData("Vault","Password","MePassword")
newMaster.addPeaPodData("Vault","Notes","Notes about me password")
newMaster.save()
"""


