#Primzahl  
#Miller - Rabin test
#Zuverlässig bis : 341.550.071.728.321

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
    # Returns exact according to http://primes.utm.edu/prove/prove2_3.html
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
    # otherwise
    return not any(_try_composite(a, d, n, s) 
                   for a in _known_primes[:_precision_for_huge_n])
#für test verschlüsslung
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
#ende für test verschlüsselung

begin = int(input('Anfang : '))
grenze = begin + int(input('Grenze, begin + x : '))

if begin%2 ==0 :
	begin = begin+1

_known_primes = [2, 3]

_known_primes += [x for x in range(begin, grenze, 2) if is_prime(x)]

#print(_known_primes) #for testing purposes enabled
#Key GEN :
n = [1]
n2 = [1]

print ('Primzahlen generiert schlüssel berechnung läuft...')
		
i = True


while i:
	d = (-1)

	while d < 0 :

		p = random.choice(_known_primes)
		q = random.choice(_known_primes)
		print('Primzahlen ausgewählt')

		if p == q:
			q = random.choice(_known_primes)

		n[0] = (p*q)

		print('N errechnet')

		n2[0] = (p-1)*(q-1)
		print('N2 errechnet')

		e =  random.randint(1, n2[0]) 
		print('E gewählt')		

		d=extendedGcd(e, n2[0])
		print('Inverse "D" errechnet')

	print('Test verschlüsselung zur funktions gewährleistung wird durchgeführt...')

	numberTrueOne = 666

	numberCypher = [1]

	numberCypher[0] = modExp(numberTrueOne, e, n[0])
	numberTrueTwo = modExp(numberCypher[0], d, n[0])

	if numberTrueOne == numberTrueTwo :
		print('Erfolgreich!')
		i = False

print("N: "+ str(n[0]))
print("E: " + str(e))
print("D: "+ str(d))


with open("publicKey.txt", "w") as text_file :
	print(str(n[0]), file=text_file)
	print(str(e), file=text_file)

with open("privateKey.txt", "w") as text_file :
	print(str(n[0]), file=text_file)
	print(str(d), file=text_file)