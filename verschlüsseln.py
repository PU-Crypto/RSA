#Verschlüsselung

import sys

m = int(input("TrueText:"))

with open("key.txt")as rfile:
	lines = rfile.readlines()[0:4]

print(lines)


print(n, e)
n=int(n)
e=int(e)

m=m**e
c=(m%n)

print("Crypted Number:")
print(c)