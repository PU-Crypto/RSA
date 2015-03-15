#Key Generation

import random

limit = int(input("Primzahlen bis ? : "))

primeList=[]

for x in range(2, limit + 1):
	isPrime = True
	for y in range(2,int(x**0.5)+1):
		if x % y == 0:
			isPrime = False
			break

	if isPrime:
		primeList.append(x)
		
d = (-1)

while d < 0 :

	p = random.choice(primeList)
	q = random.choice(primeList)

	if p == q:
		q = random.choice(primeList)

	n = p*q

	n2 = (p-1)*(q-1)

	e = (2**(2*random.randint(2,10))+1) #random Fermet nummer also 2^(2*n)+1


	#euklidischer algorithmus, quelle : GOOGLE ^^
	def extendedGcd(a,b):
		u, v, s, t = 1, 0, 0, 1
		while b>0:
			r=a//b 
			a, b = b, a-r*b 
			u, s = s, u-r*s
			v, t = t, v-r*t
		return   u

	d=extendedGcd(e, n2)

print("N:")
print(n)

print("E:")
print(e)

print("D:")
print(d)

with open("Key.txt", "w") as text_file :
	print(str(n), file=text_file)
	print(str(e), file=text_file)
	print(str(d), file=text_file)




