import random
import sys
import os
from math import sqrt, gcd
from itertools import count, islice
from functools import reduce
#from fractions import gcd

def modInverse(a, m):
    g = gcd(a, m)
    if (g != 1):
        print("Inverse doesn't exist")
        return None
    else:
        return pow(a, m - 2, m)

def lcmList(list):
    lcm = 1
    for i in list:
        lcm = lcm * i // gcd(lcm, i)
    return lcm

def gcdList(list):
    x = reduce(gcd, list)
    return x

class Fraction:
    def __init__(self, numerator, denominator):
        self.numerator = int(numerator)
        self.denominator = int(denominator)

    def print(self):
        print(self.numerator, '/', self.denominator, sep='')

    def getDecimal(self):
        return self.numerator / self.denominator

    def multiply(self, other):
        self.numerator *= other.numerator
        self.denominator *= other.denominator
        if self.denominator < 0:
            self.numerator *= -1
            self.denominator *= -1

    def add(self, other):
        self.numerator *= other.denominator
        self.denominator *= other.denominator
        other.numerator *= int(self.denominator / other.denominator)
        self.numerator += other.numerator
        self.simplify()
        if self.denominator < 0:
            self.numerator *= -1
            self.denominator *= -1

    def simplify(self):
        divisor = gcd(int(self.numerator), int(self.denominator))
        self.numerator = int(self.numerator / divisor)
        self.denominator = int(self.denominator / divisor)

class Polynomial:
    def __init__(self, *args):
        if len(args) == 1:
            parameters = args[0]
            self.t = len(parameters)
            self.s = parameters[-1]
            self.parameters = {0: self.s}
            for i in range(2, self.t + 1):
                self.parameters[i - 1] = parameters[-i]

        if len(args) == 2:
            s = args[0]
            t = args[1]
            self.s = s
            self.t = t
            lower = -1000
            upper = 1000
            self.parameters = {0: s}
            for i in range(1, t):
                self.parameters[i] = random.randrange(lower, upper + 1)

        if len(args) == 4:
            s = args[0]
            t = args[1]
            lower = args[2]
            upper = args[3]
            self.s = s
            self.t = t
            self.parameters = {0: s}
            for i in range(1, t):
                self.parameters[i] = random.randrange(lower, upper + 1)

    def calculate(self, x):
        result = 0
        for power in self.parameters:
            result += self.parameters[power] * pow(x, power)
        return result

    def print(self):
        print("f(x) = ", end='', sep='')
        for i in range(self.t - 1, -1, -1):
            if i == 0:
                print(self.parameters[i])
            elif i == 1:
                print(self.parameters[i], "x + ", end='', sep='')
            else:
                print(self.parameters[i], "x^", i, " + ", end='', sep='')

def isPrime(x):
    return x > 1 and all(x % i for i in islice(count(2), int(sqrt(x) - 1)))

def generate():
    s = None
    n = None
    t = None
    p = None
    polynomial = None

    if sys.argv[2] == "manual":
        s = int(input("s = "))
        n = int(input("n = "))
        t = int(input("t = "))
        p = int(input("p = "))

        if t > n:
            print("t MUSTN'T BE GREATER THAN n!")
            sys.exit()

        if p <= s or p <= n:
            print("p MUST BE GREATER THAN s AND n!")
            sys.exit()

        if isPrime(p) == False:
            print("p MUST BE PRIME!")
            sys.exit()

        polynomial = Polynomial(s, t, -p + 10, p - 10)
        polynomial.print()
    elif sys.argv[2] == "ready":
        s = 954
        n = 4
        t = 3
        p = 1523
        polynomial = Polynomial([62, 352, s])
        print("s =", s)
        print("n =", n)
        print("t =", t)
        print("p =", p)
        polynomial.print()
    else:
        print("WRONG ARGUMENT/-S!")
        sys.exit()

    shares = {}
    for i in range(1, n + 1):
        polynomialValue = polynomial.calculate(i)
        share = polynomialValue % p
        print("s", i, " = f(", i, ") mod p = ", share, "\n", end='', sep='')
        shares["s" + str(i)] = (i, share)

    print(shares)

def decode():
    #'''
    n = int(input("n = "))
    t = int(input("t = "))
    p = int(input("p = "))

    shares = {}
    for i in range(0, t):
        share = input("share #" + str(i + 1) + " = ")
        share = tuple(map(int, share.split(",")))
        shares[i] = share
    '''
    n = 5
    t = 3
    p = 1523
    #shares = {0: (1, 897), 1: (2, 1411), 2: (5, 1196)}
    shares = {0: (1, 19), 1: (2, 490), 2: (5, 1358)}
    #shares = {0: (1, 19), 1: (2, 490), 2: (3, 1124)}
    #'''

    print(shares)

    s = 0
    #s = Fraction(0, 1)
    for j in range(0, t):
        xj = shares[j][0]
        yj = shares[j][1]
        product = Fraction(1, 1)
        #product = 1
        for m in range(0, t):
            if j != m:
                xm = shares[m][0]
                #product *= (xm / (xm - xj))
                factor = Fraction(xm, xm - xj)
                product.multiply(factor)
                product.simplify()
        #s += (yj * product.numerator)
        numerator = product.numerator
        denominator = product.denominator
        s += yj * numerator * modInverse(denominator, p)

    s = s % p

    print("SECRET s =", s)

def main():
    #os.system("cls")

    if sys.argv[1] == "generate":
        generate()
    elif sys.argv[1] == "decode":
        decode()
    else:
        print("WRONG ARGUMENT/-S!")

if __name__ == '__main__':
    main()