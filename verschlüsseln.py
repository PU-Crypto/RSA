#Verschlüsselung

import sys

m = int(input("TrueText:"))

with open("key.txt")as rfile:
	lines = rfile.readlines()[0:4]

n = int(lines[0])
e = int(lines[1])

m=m**e
c=(m%n)

print("Crypted Number:")
print(c)