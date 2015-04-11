#NEW PRIME GENERATOR
#CULLEN PRIMES
#

def fak(a): #fakultät
	b = a
	while b > 0:
		a = a*b
		b -= b 
	return a


cap = int(input("Grenze : "))

x = 0

prime = []
for x in range(cap+1):
	prime.append(x*(2**x)+1)
	prime.append(fak(fak(x**2))+1)

print(prime)


#
