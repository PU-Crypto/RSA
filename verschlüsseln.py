#Verschlüsselung

import sys

#implemention begin
# source : https://gist.github.com/avalonalex/2122098

def int2baseTwo(x): #ermöglicht rechnung mit sehr großen zahlen bei geringen ressourcen
    # x is a positive integer. Convert it to base two as a list of integers in reverse order."""
    # repeating x >>= 1 and x & 1 will do the trick
    assert x >= 0
    bitInverse = []
    while x != 0:
        bitInverse.append(x & 1)
        x >>= 1
    return bitInverse

def modExp(a, d, n): # Expnentiale modulo rechnung (a ** d (mod n)) ermöglicht schnelle rechnung mit Werten über Integergrenze
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
    return result % n

#implementation end

text = input("TrueText als Buchstaben: ") #Zuverschlüsselnder Text nur UTF-8 unterstütze Zeichen

text=text.encode('utf-8') #Jedes Zeichen wird durch seine Kennnummer ersetzt : Hallo => H:72, a:97, l:108, l:108, o:111=> 72, 97, 108, 108, 111
list(text)
sammlung = []

for i in range(0,len(text)): #Zahlen werden nun in eigene Array position geschrieben 
        dump=text[i]
        sammlung.append(dump)

print(sammlung) #Hallo würde jetzt so vorliegen : [72, 97, 108, 108, 111]

with open("publicKey.txt")as rfile: #Public-Key wird aus der datei publicKey.txt ausgelesen
	lines = rfile.readlines()[0:2] #beginnent bei Zeile 0 und insgesamt 2 Zeilen (Zeile 1-2) Nach unserer Zählform

n = int(lines[0])
e = int(lines[1])

for x in range(0,(len(sammlung))):
	sammlung[x] = modExp(sammlung[x], e, n) #Jede Array position wird einzeln verschlüsselt mit dem eingelesenen Key und überschreibt die originale Nummer

print("Crypted list:") #Für den nutzer wird die Verschlüsselte folge gezeigt (kann auskommentiert werden)
print(sammlung)

with open("cypher.txt", "w") as text_file : #Cypher wird gespeichert in Cypher.txt
	print(str(len(sammlung)), file=text_file) #Die erste Zeile ist eine Zahl die die anzahl der zu erwartenden Zeichen (Anzahl der Arraypositionen) wiedergibt zum entschlüsseln wichtig
	for x in range(0,len(sammlung)):
		print(str(sammlung[x]), file=text_file) #Weitere Zeilen geben nun die verschlüsselten zeichen wieder wobei eine Zeile genau ein Zeichen entspricht 