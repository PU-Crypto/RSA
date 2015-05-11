#Entschlüsselung
#implemention begin
# source : https://gist.github.com/avalonalex/2122098
import json

def int2baseTwo(x): #ermöglicht rechnung mit sehr großen zahlen bei geringen ressourcen
    # x is a positive integer. Convert it to base two as a list of integers in reverse order."""
    # repeating x >>= 1 and x & 1 will do the trick
    assert x >= 0
    bitInverse = []
    while x != 0:
        bitInverse.append(x & 1)
        x >>= 1
    return bitInverse
 
 
def modExp(a, d, n): # Expnonentiale modulo rechnung (a ** d (mod n)) ermöglicht schnelle rechnung mit Werten über Integergrenze
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
name = input('Wer bin ich? :' )

with open(name+".json")as f:
	Key = json.load(f)
	n = int(Key['n' ])
	d = int(Key['d' ])

with open("cypher.txt")as rfile: #Aus der Cypher.txt wird die Anzahl der zuerwartenden Zeichen wieder
	grenze = int(rfile.readlines()[0])

with open("cypher.txt")as rfile: #Zeichen selbst von Zeile 2 bis zur Anzahl der Zeichen + 1
		sammlung = rfile.readlines()[1:int(grenze)+1]

for x in range(0,len(sammlung)): #Eingelesene Zeichen werden von String zu Integer formatiert 
	sammlung[x] = int(sammlung[x])	


for x in range(0,len(sammlung)): #Entschlüsselung
	sammlung[x] = modExp(sammlung[x], d, n)
	
print(sammlung) #Entschlüsselte Zeichen liegen in Array vor 
text = ''

for x in range(0,len(sammlung)): 
	sammlung[x] = chr(sammlung[x]) #Zeichen werden von Zahl zu Buchstabe gewandelt
	text = text+sammlung[x] #Buchstaben werden in einen String geschrieben [H, a, l, l, o] => 'Hallo'

print(text) #Entschlüsselter Text wird dem Nutzer gezeigt

with open("Truetext.txt", "w")as rfile: #Text wird gespeichert in Truetext.txt 
	print(text, file =rfile)
