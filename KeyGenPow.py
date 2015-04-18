#Primzahl  
#Miller - Rabin test
#Zuverlässig bis : 341.550.071.728.321 höhere zahlen möglicher weise nur pseudoprimzahlen

import random

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
 
def is_prime(n, _precision_for_huge_n=16):
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

#für test verschlüsslung
def int2baseTwo(x):
    """x is a positive integer. Convert it to base two as a list of integers
    in reverse order as a list."""#ermöglicht rechnung mit sehr großen zahlen bei geringen ressourcen Quelle : https://gist.github.com/avalonalex/2122098
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
#ende für test verschlüsselung

begin = int(input('Anfang : ')) #Input wert
grenze = begin + int(input('Grenze, begin + x : ')) # Schritte weiter von dem Input


if begin%2 ==0 :   # Sollte begin mod(2) =0 ergeben so ist begin durch 2 restlos teilbar (begin muss für die funktion ungerade sein)
	begin = begin+1

_known_primes = [2, 3] #grund primzahlen zum ermitteln anderer benötigt

_known_primes += [x for x in range(begin, grenze, 2) if is_prime(x)] #Primzahl test verfahren ausgefürt mit jeder ungeraden (jeder 2ten) Zahl

#print(_known_primes) #Gibt alle gefundenen Primzahlen an

n = [1] #da die zahlen N (p*q) und N2(p-1*q-1) die grenzen des Integers überschreiten werden sie in eine Array position gespeichert (Zeichenfolge mit nciht relevanter genze)
n2 = [1]

print ('Primzahlen generiert schlüssel berechnung läuft...')
		
i = True #Als bedingung für die Testverschlüsselung

while i:
	d = (-1) # Als bedingung für nur positive Inverse zu N2

	while d < 0 :

		p = random.choice(_known_primes) #Primzahl wird pseudozufällig aus allen überprüften Zahlen gewählt
		q = random.choice(_known_primes)
		while p == q:
			q = random.choice(_known_primes)
		print('Primzahlen ausgewählt')

		n[0] = (p*q)
		print('N errechnet')

		n2[0] = (p-1)*(q-1)
		print('N2 errechnet')

		e =  random.randint(1, n2[0]) 
		print('E gewählt')		

		d=extendedGcd(e, n2[0])
		print('Inverse "D" errechnet')

	print('Test verschlüsselung zur funktions gewährleistung wird durchgeführt...')

	numberTrueOne = 666 #Beliebige Zahl für die Test verschlüsselung (50-999 da eine UTF-8 realistische zahlen größe gegeben sein soll)

	numberCypher = [1] #Verschlüsselte Zahl überschreitet ggf. Integer grenze => Array position

	numberCypher[0] = modExp(numberTrueOne, e, n[0]) #Beliebige Zahl (numberTrueOne) wird verschlüsselt und in numberCypher[0] abgespeichert
	numberTrueTwo = modExp(numberCypher[0], d, n[0]) #numberCypher[0] wird wieder entschlüsselt und in numberTrueTwo abgespeichert

	if numberTrueOne == numberTrueTwo : #Wenn die Zahl Vor und nach Ver- und Entschlüsselung die selbe ist wahr der Test Erfolgreich
		print('Erfolgreich!')
		i = False

print("N: "+ str(n[0])) #Relevante Werte werden dem Nutzer gezeigt kann auskommentiert werden
print("E: " + str(e))
print("D: "+ str(d))



with open("publicKey.txt", "w") as text_file : #Public-Key umfasst : N, E wird abgepseichert in publicKey.txt
	print(str(n[0]), file=text_file)
	print(str(e), file=text_file)

with open("privateKey.txt", "w") as text_file : #Private-Key umfasst : N, D wird abgespeichert ind privateKey.txt
	print(str(n[0]), file=text_file)
	print(str(d), file=text_file)