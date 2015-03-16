#Entschlüsselung

c = int(input("Crypted Text:"))

with open("privatekey.txt")as rfile:
	lines = rfile.readlines()[0:2]

n = int(lines[0])

d = int(lines[1])


c=c**d
m=(c%n)

print("Original Number:")
print(m)