#Entschlüsselung


with open("privatekey.txt")as rfile:
	lines = rfile.readlines()[0:2]
n = int(lines[0])
d = int(lines[1])

with open("cypher.txt")as rfile:
	grenze = int(rfile.readlines()[0])

with open("cypher.txt")as rfile:
		sammlung = rfile.readlines()[1:int(grenze)+1]

for x in range(0,len(sammlung)):
	sammlung[x] = int(sammlung[x])

for x in range(0,len(sammlung)):
	sammlung[x]=sammlung[x]**d
	sammlung[x]=sammlung[x]%n

print("Original Array:")
print(sammlung)

text = ''

for x in range(0,len(sammlung)):
	sammlung[x] = chr(sammlung[x])
	text = text+sammlung[x]

print(text)

with open("Truetext.txt", "w")as rfile:
	print(text, file =rfile)
