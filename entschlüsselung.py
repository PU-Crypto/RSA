#Entschlüsselung

c = int(input("Crypted Text:"))

with open("key.txt")as rfile:
	lines = rfile.readlines()[0:4]

n = int(lines[0])

d = int(lines[2])


c=c**d
m=(c%n)

print("Original Number:")
print(m)