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


#====================Functions====================
"""
These functions are used for generating passwords, 
and also encrypting and decrypting data.
"""

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



