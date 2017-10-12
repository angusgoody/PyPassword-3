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
#====================Core Classes====================
"""
The PEM core classes are the classes that form the basic 
structure of PyPasswords security, they are the classes
the sensitive data is stored in.
"""

class pod:
	"""
	A pod is what
	each account in PyPassword
	is stored in.
	"""
	def __init__(self,master,podTitle):
		self.master=master
		self.podTitle=podTitle
		self.podVault={}

	def addData(self,):

class masterPod:
	"""
	The vault contains
	all a users accounts which
	are individually called Pods
	"""
