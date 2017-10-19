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

#====================Log====================
class log:
	"""
	The log is a way of recording
	events that go on throughout 
	the program. Each file has its own
	log which it reports to during runtime
	"""
	logs={}
	def __init__(self,logName):
		self.logName=logName
		#Add the log to all logs
		log.logs[logName]=self
		#Store the data
		self.systemData={}
		self.generalData={}
		#Store tags
		self.tags={}

	def report(self,message,*extra,**kwargs):
		"""
		The report method reports
		 a problem or event to the 
		 log.
		"""
		#Variables
		dataDictionary=self.generalData
		tag="Default"

		#Create message string
		if len(extra) > 0:
			for item in extra:
				message+=str(item)
				message+=" "

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
		This method will save the log
		to file using pickle. It can then
		viewed and loaded in PyPassword, 
		error and default data will only be saved
		to file to save space.
		"""
		fileName=self.logName+"Log.log"
		#Open the file
		file=open("PyLogs/"+fileName,"a")

		#Save the default data
		for item in self.generalData:
			writeString=str(self.generalData[item])
			writeString+=","
			writeString+=item
			writeString+=",Default\n"
			file.write(writeString)

		#Close file
		file.close()

#Initiate PEM log
log=log("Encryption")
#====================Functions====================
"""
These functions are used for generating passwords, 
and also encrypting and decrypting data.
"""

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
	a pickle file
	"""
	pickle.dump(content, open( fileName, "wb" ) )
	log.report("Save complete exported to",fileName,tag="File")

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
		self.master=master
		self.podName=podName

class masterPod:
	"""
	The master pod class is the class
	which stores all the smaller data
	for every account stored in PyPassword
	"""
	def __init__(self,name):
		self.masterName=name
		self.children={}



