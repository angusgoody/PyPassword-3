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
from Crypto.Cipher import AES

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
			encryptionKey=self.master.key
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
		#Store the key used during runtime
		self.key=None
		#Key used for checking master key
		self.checkKey="key"
		#Store the hint
		self.hint="No Hint Available"
		#Where the pods are stored
		self.peas={}
		#Store currently loaded pea pod
		self.currentPeaPod=None
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
		#Close the pod (Encrypt etc)
		self.close()

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
		print("Closing")
		#Ensure all pods are secure
		for podName in self.peas:
			pod=self.peas[podName]
			if pod.vaultState == False:
				pod.unlockVault("Lock")

		#Encrypt the key to a vaule which can only be decrypted with current key
		self.checkKey=encrypt("key",self.key)
		self.key=None


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

def checkMasterPodPassword(masterPodInstance,attempt):
	"""
	Will check the password attempt of a certain
	master pod.
	Returns true if the password is correct
	Return false is the password is incorrect
	"""
	if type(masterPodInstance) == masterPod:
		#Decrypt the key
		decryptResult=decrypt(masterPodInstance.checkKey,attempt)
		#If the result is not None then it was correct
		if decryptResult:
			#Add key to master pod for use later on
			masterPodInstance.key=attempt
			return True
		else:
			return None

#====================Testing area====================

"""
pods=["Amazon","Google","Spotify","Souncloud","PyCharm","Wix","Argos","King Edwards"]


names={"Simon":"Angy","Sam":"gay","Bob":"Bob"}


hints=["A secret hint","Ahahhah me","Never guess me password"]
for item in names:
	newPod=masterPod(item)
	newPod.key=names[item]
	newPod.hint=hints.pop()

	podName=pods.pop()
	newPod.addPeaPod(podName)

	newPod.addPeaPodData(podName,"Password","Secret")
	newPod.save()


#""

newMasterPod=masterPod("NewBoi")
newMasterPod.key="boi123"
newMasterPod.hint="Boi with 123"

newMasterPod.addPeaPod("my notes",template="SecureNote")
newMasterPod.addPeaPodData("my notes","Title","My note")
newMasterPod.addPeaPodData("my notes","Note","The content of my note")

newMasterPod.addPeaPod("Github")
newMasterPod.addPeaPodData("Github","Username","Angusgoody")
newMasterPod.addPeaPodData("Github","Password","angy123")
newMasterPod.addPeaPodData("Github","Website","github.com")

newMasterPod.save()

"""
