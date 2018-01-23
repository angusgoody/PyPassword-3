
#Testing

#Imports
from PyUi import searchDataSource

myList=["Angus","Bob","Damn","daniel",["Sam","Katie",{"MyName":"Turtle"}]]

searches=["angus","cat","DaMn","Hi","Bob","tUrtle"]

for item in searches:
	print(searchDataSource(item,myList,capital=True))

