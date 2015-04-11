#Verschlüsselung

import sys

text = input("TrueText als Buchstaben:")

text=text.encode('utf-8')
list(text)
sammlung = []

for i in range(0,len(text)): #erstelle einen array mit zahlen 
        dump=text[i]
        sammlung.append(dump)
print(sammlung)

with open("publicKey.txt")as rfile:
	lines = rfile.readlines()[0:2]

n = int(lines[0])
e = int(lines[1])


for x in range(0,(len(sammlung))):
	sammlung[x]=sammlung[x]**e
	sammlung[x]=(sammlung[x]%n)

print("Crypted list:")

print(sammlung)

with open("cypher.txt", "w") as text_file :
	print(str(len(sammlung)), file=text_file)
	for x in range(0,len(sammlung)):
		print(str(sammlung[x]), file=text_file)