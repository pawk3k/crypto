import numpy as np


from random import randint


# trivial method for secret splitting
def trivialCy(secret, k):
    random_values = []
    for _ in range(2):
        random_values.append(randint(0, k))
    last = (secret - sum(random_values)) % k
    random_values.append(last)
    print("Crypted",  random_values)
    print("Decryted:", sum(random_values) % k)


def shamirDeCy(Bmatrix, indexes, t, prime):
    outArr = []
    for index in indexes:
        correctInd = index + 1
        outArr.append(
            [correctInd**innerIndex for innerIndex in range(t)])

    a = np.array(outArr)
    print(outArr)
    b = np.array(Bmatrix)
    b = b.take(indexes)
    x = np.linalg.solve(a, b)
    return x[0] % prime


def isPrime(n):
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True


def generatePrime():
    while True:
        p = randint(1, 10000)
        if isPrime(p):
            return p


def shamirCy(s, n, t):
    prime = generatePrime()
    random_values = []
    for _ in range(t - 1):
        random_values.append(randint(0, 100000))
    print(random_values)
    den_ = [sum(
        [item * x**i for i, item in enumerate([s, *random_values])]) % prime
        for x in range(1, n+1)]
    print("podzialy:", den_)
    print("Decryted:", shamirDeCy(den_, [0, 1, 2], t, prime))
    return 0


# inverse
print("trivial")
trivialCy(456, 1000)
print("shamir")
shamirCy(954, 4, 3)
