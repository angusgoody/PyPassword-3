
import pickle
import PEM

files=PEM.findFiles(PEM.getWorkingDirectory(),".mp")

for file in files:
	masterPod=pickle.load( open( file, "rb" ) )
	#Get the pea pods
	pods=masterPod.peas
	#Get the encryption key
	key=masterPod.key
	print("Key:",key)
