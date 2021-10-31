import numpy as np
from scipy import linalg
from sympy import poly
from sympy import symbols
from sympy import Poly
from sympy.abc import s


from random import randint


def shamirDeCy(Bmatrix, indexes, t):
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
    return x[0] % 1523


def shamirCy(s, n, t):
    # p = randint(s, 10000)
    # p - prime number
    p = 1523
    # a1 = randint(0, s)
    random_values = []
    for _ in range(t - 1):
        random_values.append(randint(0, 100000))
    print(random_values)
    den_ = [sum(
        [item * x**i for i, item in enumerate([s, *random_values])]) % p
        for x in range(1, n+1)]
    print(den_)
    print(shamirDeCy(den_, [0, 4], t))
    return 0


shamirCy(200, 5, 2)
