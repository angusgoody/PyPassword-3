
from PEM import decrypt,encrypt

print(encrypt("Angus123","turtle"))

data=input("Enter data to decrypt: ")
key=input("Enter key: ")

print(decrypt(data,key))