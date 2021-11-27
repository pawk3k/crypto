import sys
import os
import random

def generate():
    s = None
    n = None
    k = None

    if sys.argv[2] == "manual":
        s = int(input("s = "))
        n = int(input("n = "))
        k = int(input("k = "))

        if s < 0 or s >= k:
            print("s MUST BE IN <0, k - 1>!")
            sys.exit()

    elif sys.argv[2] == "ready":
        s = 456
        n = 3
        k = 1000
        print("s =", s)
        print("n =", n)
        print("k =", k)

    else:
        print("WRONG ARGUMENT/-S!")
        sys.exit()

    shares = {}
    total = 0
    for i in range(0, n - 1):
        share = random.randrange(0, k)
        total += share
        shares[i] = share
        print("s" + str(i) + " = " + str(share))

    shares[n - 1] = (s - total) % k
    print("s" + str(n - 1) + " = (" + str(s), end='')
    for i in range(0, n - 1):
        print(" - " + str(shares[i]), end='')
    print(") mod " + str(k) + " = " + str(shares[n - 1]))

    print(shares)

def decode():
    n = int(input("n = "))
    k = int(input("k = "))

    shares = {}
    total = 0
    for i in range(0, n):
        share = int(input("share #" + str(i + 1) + " = "))
        shares[i] = share
        total += share

    print(shares)

    s = total % k

    print("SECRET s =", s)

def main():
    os.system("cls")

    if sys.argv[1] == "generate":
        generate()
    elif sys.argv[1] == "decode":
        decode()
    else:
        print("WRONG ARGUMENT/-S!")

if __name__ == '__main__':
    main()