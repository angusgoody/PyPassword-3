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

		#Get working directory
		currentDirectory=getWorkingDirectory()
		#Create file name
		fileName=currentDirectory+"/"+"/PyLogs"+"/"+fileName
		#If the directory does not exist create it
		if not os.path.isdir(currentDirectory+"/PyLogs"):
			os.makedirs(currentDirectory+"/PyLogs")

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

def getWorkingDirectory():
	currentDirectory=os.path.dirname(os.getcwd())

def openPickle(fileName):
	"""
	This function opens a pickle file
	and returns the content
	"""
	try:
		content=pickle.load( open( fileName, "rb" ) )
	except:
		logClass.report("Error reading file when pickling")
		return None
	else:
		return content

def savePickle(content,fileName):
	"""
	This function will dump
	a pickle file
	"""
	pickle.dump(content, open( fileName, "wb" ) )
	log.report("Save complete exported to", fileName, tag="File")

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

class pod:
	"""
	The pod class is a class
	for each account stored in PyPasssword.
	It will securely store data using
	encryption
	"""
	def __init__(self,master,podName):
		#Store the parent master pod
		self.master=master
		#Name of the pod
		self.podName=podName
		#Encrypted vault where info is stored
		self.vault={}
		#Store template type
		self.templateType="Login"
		#Store Vault state
		self.vaultState="Unlocked"

	def unlockVault(self,unlockOrLock):
		"""
		This method will secure the pod vault
		and encrypt all the data inside ready
		to save to file
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
			#Iterate through pod
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
		else:
			log.report("Attempted to encrypt locked vault")


class masterPod:
	"""
	The master pod class is the class
	which stores all the smaller data
	for every account stored in PyPassword
	"""
	def __init__(self,name):
		#Name of the master pod
		self.masterName=name
		#Where the pods are stored
		self.pods={}
		#The master key used for encryption
		self.masterKey=None





