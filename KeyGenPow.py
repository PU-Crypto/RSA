#Primzahl  
#Miller - Rabin test
#Zuverlässig bis : 341.550.071.728.321

import random

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

begin = int(input('Anfang : '))
grenze = begin + int(input('Grenze, begin + x : '))

if begin%2 ==0 :
	begin = begin+1

_known_primes = [2, 3]

_known_primes += [x for x in range(begin, grenze, 2) if is_prime(x)]

print(_known_primes) #for testing purposes enabled
#Key GEN :
n = [1]
n2 = [1]

print ('Primzahlen generiert schlüssel berechnung läuft...')
		
d = (-1)

while d < 0 :

	p = random.choice(_known_primes)
	q = random.choice(_known_primes)

	if p == q:
		q = random.choice(_known_primes)

	n[0] = (p*q)

	n2[0] = (p-1)*(q-1)

	e = (2**(2*random.randint(2,50))+1) #random Fermet nummer also 2^(2*n)+1
	while e > n2[0] or e < (n2[0]*0.25):
		e = (2**(2*random.randint(2,50))+1) #random Fermet nummer also 2^(2*n)+1
	#e =  random.randint(1, n2[0]) 

	#euklidischer algorithmus, quelle : GOOGLE ^^
	def extendedGcd(a,b):
		u, v, s, t = 1, 0, 0, 1
		while b>0:
			r=a//b 
			a, b = b, a-r*b 
			u, s = s, u-r*s
			v, t = t, v-r*t
		return   u

	d=extendedGcd(e, n2[0])

print("N: "+ str(n[0]))
print("E: " + str(e))
print("D: "+ str(d))


with open("publicKey.txt", "w") as text_file :
	print(str(n[0]), file=text_file)
	print(str(e), file=text_file)

with open("privateKey.txt", "w") as text_file :
	print(str(n[0]), file=text_file)
	print(str(d), file=text_file)