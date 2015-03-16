#Verschlüsselung

import sys

m = int(input("TrueText:"))

with open("publicKey.txt")as rfile:
	lines = rfile.readlines()[0:2]

n = int(lines[0])
e = int(lines[1])

m=m**e
c=(m%n)

print("Crypted Number:")
print(c)