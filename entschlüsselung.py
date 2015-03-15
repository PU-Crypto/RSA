#Entschlüsselung

c = int(input("Crypted Text:"))

d = int(input("SecretKey:"))

n = int(input("PublicKey:"))

c=c**d
m=(c%n)

print("Original Number:")
print(m)