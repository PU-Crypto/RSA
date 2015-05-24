# -*- coding: utf-8 -*-
import sys
import random
import json
import os
from os import path



#Hilfsfunktionen 

def extendedGcd(a,b):
		u, v, s, t = 1, 0, 0, 1
		while b>0:
			r=a//b 
			a, b = b, a-r*b 
			u, s = s, u-r*s
			v, t = t, v-r*t
		return   u

def _try_composite(a, d, n, s):
    if pow(a, d, n) == 1:
        return False
    for i in range(s):
        if pow(a, 2**i * d, n) == n-1:
            return False
    return True # n  is definitely composite
 
def is_prime(_known_primes, n, _precision_for_huge_n=16):
    if n in _known_primes or n in (0, 1):
        return True
    if any((n % p) == 0 for p in _known_primes):
        return False
    d, s = n - 1, 0
    while not d % 2:
        d, s = d >> 1, s + 1
    # gibt teilbarkeit nach : http://primes.utm.edu/prove/prove2_3.html
    if n < 1373653: 
        return not any(_try_composite(a, d, n, s) for a in (2, 3))
    if n < 25326001: 
        return not any(_try_composite(a, d, n, s) for a in (2, 3, 5))
    if n < 118670087467: 
        if n == 3215031751: 
            return False
        return not any(_try_composite(a, d, n, s) for a in (2, 3, 5, 7))
    if n < 2152302898747: 
        return not any(_try_composite(a, d, n, s) for a in (2, 3, 5, 7, 11))
    if n < 3474749660383: 
        return not any(_try_composite(a, d, n, s) for a in (2, 3, 5, 7, 11, 13))
    if n < 341550071728321: 
        return not any(_try_composite(a, d, n, s) for a in (2, 3, 5, 7, 11, 13, 17))
    # falls größer als 341.550.071.728.321
    return not any(_try_composite(a, d, n, s) 
                   for a in _known_primes[:_precision_for_huge_n])

def int2baseTwo(x):
    #x is a positive integer. Convert it to base two as a list of integers in reverse order as a list.
    #ermoeglicht rechnung mit sehr großen zahlen bei geringen ressourcen Quelle : https://gist.github.com/avalonalex/2122098
    # repeating x >>= 1 and x & 1 will do the trick
    assert x >= 0
    bitInverse = []
    while x != 0:
        bitInverse.append(x & 1)
        x >>= 1
    return bitInverse
 
def modExp(a, d, n):
    #returns a ** d (mod n)
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

#Hilfsfunktionen ende

def keygen(name):
	begin = random.randint( pow(2, 1024), pow(2, 1025) ) #Startwert bei 2^2048 werden 1024bit keys generiert

	grenze = begin + 20000 # Schritte weiter von dem Input min 10.000 default = 20.000

	if begin%2 ==0 :   # Sollte begin rest los durch 2 teilbar sein, kann die Funktion nciht ausgefuehrt werden
		begin = begin+1

	_known_primes = [2,3] #grund Primzahlen zum ermitteln anderer benötigt

	_known_primes += [x for x in range(begin, grenze, 2) if is_prime(_known_primes, x)] #Primzahl test verfahren ausgefürt mit jeder ungeraden (jeder 2ten) Zahl

	# print(_known_primes) #Gibt alle gefundenen Primzahlen an 

	n = [1] #da die zahlen N (p*q) und N2(p-1*q-1) die grenzen des Integers ueberschreiten werden sie in eine Array position gespeichert (Zeichenfolge mit nciht relevanter genze)
	n2 = [1]

	#print ('Primzahlen generiert schluessel berechnung laeuft...')
	#print(_known_primes)
			
	i = True #Als bedingung für die Testverschluesselung

	while i:
		d = (-1) # Als bedingung für nur positive Inverse zu N2

		while d < 0 :

			p = random.choice(_known_primes) #Primzahl wird pseudozufaellig aus allen überprueften Zahlen gewaehlt
			q = random.choice(_known_primes)

			while p==2 or p==3:
				p = random.choice(_known_primes)

			while q==2 or q==3:
				q = random.choice(_known_primes)

			#print('Primzahlen ausgewaehlt')
			#print(p)
			#print(q)

			n[0] = (p*q)
			#print('N errechnet')

			n2[0] = (p-1)*(q-1)
			#print('N2 errechnet')

			e =  65537
			#print('E gewaehlt')		

			d=extendedGcd(e, n2[0])
			#print('Inverse "D" errechnet')

		#print('Key Berechnung Abgeschlossen.\n Test verschluesselung zur funktions gewaehrleistung wird durchgeführt...')

		numberTrueOne = 666 #Beliebige Zahl für die Test verschluesselung (50-999 da eine UTF-8 realistische zahlen groeße gegeben sein soll)

		numberCypher = [1] #Verschluesselte Zahl überschreitet Integer grenze => Array position

		numberCypher[0] = modExp(numberTrueOne, e, n[0]) #Beliebige Zahl (numberTrueOne) wird verschlüsselt und in numberCypher[0] abgespeichert
		numberTrueTwo = modExp(numberCypher[0], d, n[0]) #numberCypher[0] wird wieder entschlüsselt und in numberTrueTwo abgespeichert

		if numberTrueOne == numberTrueTwo : #Wenn die Zahl Vor und nach Ver- und Entschlüsselung die selbe ist wahr der Test Erfolgreich
			#print('Erfolgreich!')
			i = False
		else :
			print('Testverschlüsselung fehlerhaft wird erneut versucht...')

	print('Private-Key :'+str(n[0])+str(d) +'\n Public-Key :'+str(n[0])+str(e)  ) 

	Key = {'n': str(n[0]), 'd': str(d), 'e': str(e) }

	key_path = path.relpath("keys/" + name + ".json")
	with open(key_path, "w") as f :
		json.dump(Key, f)
#KeyGen Funktion Ende

def verschl(name, text):

	try :
		#with open(name+".json")as f:
		with open(name) as f:
			Key = json.load(f)
			n = int(Key['n' ])
			e = int(Key['e' ])
	except OSError:
		print('Fehler, kein Key für diesen Namen')
		sys.exit()

	#text = input("TrueText als Buchstaben: ") #Zuverschlüsselnder Text nur UTF-8 unterstütze Zeichen

	sammlung = [] 

	for i in range(0,len(text)): #Jede Zahl wird in eine Array position geschrieben 
	        dump=ord(text[i])
	        sammlung.append(dump)

	for x in range(0,(len(sammlung))):
		sammlung[x] = modExp(sammlung[x], e, n) #Jede Array position wird einzeln verschlüsselt mit dem eingelesenen Key und überschreibt die originale Nummer

	#print("Crypted list:") #Für den nutzer wird die Verschlüsselte folge gezeigt (kann auskommentiert werden)

	#print(sammlung)

#	with open(name+"_cypher.txt", "w") as text_file : #Cypher wird gespeichert in Cypher.txt
#		print(str(len(sammlung)), file=text_file) #Die erste Zeile ist eine Zahl die die anzahl der zu erwartenden Zeichen (Anzahl der Arraypositionen) wiedergibt zum entschlüsseln wichtig
#		for x in range(0,len(sammlung)):
#			print(str(sammlung[x]), file=text_file) #Weitere Zeilen geben nun die verschlüsselten zeichen wieder wobei eine Zeile genau ein Zeichen entspricht 
	einString=''
	einString=(str(len(sammlung))+',')
	for x in range(0, len(sammlung)):
		einString+=(str(sammlung[x])+',')

	print(einString)
#Verschlüsselung Funktion Ende

def entschl(name, text):
	try :
		with open(name)as f:
			Key = json.load(f)
			n = int(Key['n' ])
			d = int(Key['d' ])
	except OSError:
		print('Fehler, kein Key für diese Namen vorhanden')
		sys.exit()
	try:
		grenze = int(text.split(',')[0])
	except IndexError :
		print('Fehlerhafte Eingabe')
		sys.exit()
	
	sammlung = []


	for x in range(1, grenze+1):
		foo = text
		foo = foo.split(',')[x]
		foo.replace(',', '')
		sammlung.append(int(foo))

	#for x in range(0,len(sammlung)): #Eingelesene Zeichen werden von String zu Integer formatiert 
	#	sammlung[x] = int(sammlung[x])	


	for x in range(0,len(sammlung)): #Entschlüsselung
		sammlung[x] = modExp(sammlung[x], d, n)
		if x == 0:
			if sammlung[x].length() > 5 : #Bei Falschem key währe der entschlüsselte Wert über 5 stellen lang (nur mit dem richtigen key kommt es zur UTF-8 reochweite)
				print('Entschlüsselung unmöglich, ggf. ist der falsche Key ausgewählt oder ein Fehler in der Eingabe')
				sys.exit()
		
	#print(sammlung) #Entschlüsselte Zeichen liegen in Array vor 
	text = ''

	for x in range(0,len(sammlung)): 
		sammlung[x] = chr(sammlung[x]) #Zeichen werden von Zahl zu Buchstabe gewandelt
		text = text+sammlung[x] #Buchstaben werden in einen String geschrieben [H, a, l, l, o] => 'Hallo'

	print(text) #Entschlüsselter Text wird dem Nutzer gezeigt

#	with open(name+"_Truetext.txt", "w")as rfile: #Text wird gespeichert in Truetext.txt 
#		print(text, file =rfile)

#Entschlüsselung Funktion Ende

def handleShellParam(param, default):

	for cmdarg in sys.argv:
		if(("--" + param + "=") in cmdarg):
			return str(cmdarg.replace(("--" + param + "="), ""))
		elif(("-" + param + "=") in cmdarg):
			return str(cmdarg.replace(("-" + param + "="), ""))
		elif(("--" + param) in cmdarg):
			return str(cmdarg.replace(("--"), ""))
		elif(("-" + param) in cmdarg):
			return str(cmdarg.replace(("-"), ""))
	return default

#Ende FUnktionen

modus = handleShellParam("m", 0) #Modus Abfrage kann annehmen : 1=KeyGen, 2=Verschluesseln, 3=Entschluesseln
name = handleShellParam("n", 0) #Namen Abfrage 
text = handleShellParam("t", 0)

if modus == 0 and name == 0:
	print("Keine gültigen Aufrufparameter gegeben!")
	sys.exit()

elif modus == 0:
	print("Kein Modus gewählt!")
	sys.exit()

elif name == 0:
	print("Kein Name angegeben!")
	sys.exit()

elif modus == '1':
	keygen(name)
	sys.exit()

elif modus == '2':
	verschl(name, text)
	sys.exit()

elif modus == '3':
	entschl(name, text)
	sys.exit()