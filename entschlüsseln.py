#Entschlüsselung
#implemention begin
# source : https://gist.github.com/avalonalex/2122098

def int2baseTwo(x):
    """x is a positive integer. Convert it to base two as a list of integers
    in reverse order as a list."""
    # repeating x >>= 1 and x & 1 will do the trick
    assert x >= 0
    bitInverse = []
    while x != 0:
        bitInverse.append(x & 1)
        x >>= 1
    return bitInverse
 
 
def modExp(a, d, n):
    """returns a ** d (mod n)"""
    assert d >= 0
    assert n >= 0
    base2D = int2baseTwo(d)
    base2DLength = len(base2D)
    modArray = []
    result = 1
    for i in range(1, base2DLength + 1):
        if i == 1:
            modArray.append(a % n)
        else:
            modArray.append((modArray[i - 2] ** 2) % n)
    for i in range(0, base2DLength):
        if base2D[i] == 1:
            result *= base2D[i] * modArray[i]
    return result%n

#implemention end

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
	sammlung[x] = modExp(sammlung[x], d, n)
	
print(sammlung)
text = ''

for x in range(0,len(sammlung)):
	sammlung[x] = chr(sammlung[x])
	text = text+sammlung[x]

print(text)

with open("Truetext.txt", "w")as rfile:
	print(text, file =rfile)
