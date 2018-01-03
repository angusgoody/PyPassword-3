
import pickle
import PEM

files=PEM.findFiles(PEM.getWorkingDirectory(),".mp")

for file in files:
	masterPod=pickle.load( open( file, "rb" ) )
	print("\n---Opening",masterPod.masterName,"---")
	print(masterPod.__dict__)
