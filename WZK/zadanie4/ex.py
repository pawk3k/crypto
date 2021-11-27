'''
1.
Ciąg pseudolosowy ma w większości przypadków wszystkie cechy statystyczne
charakterystyczne dla ciągów losowych, lecz są powtarzalne, ze względy na to,
że są generowane przez skończone algorytmy deterministyczne, korzystające jedynie z
pewnych losowych danych wejściowych (ziarno/seed). Można to porównać w pewnym sensie do
rozwinięć dziesiętnych liczb wymiernych oraz niewymiernych. Liczby wymierne takie jak np.
331/7 = 47.28571428571428571428571428571428571428... są "losowe" w pewnym odcinku, jednak
po przecinku po prostu ten "losowy" statystycznie fragment się zapętla:
331/7 = 47.(285714). Fragmenty takie mogą być dowolnie długie, ale zawsze będą
się powtarzać, można rzec, przez skończoność definicji arytmetycznej takiej liczby.
Z kolei liczby niewymierne, takie jak pierwiastek z 2 czy pi można arytmetycznie zdefiniować
jedynie przy pomocy definicji wszystkich cyfr, albo przy pomocy nieskończonych ciągów
(jak np. problem bazylejski). W liczbach takich nie występuje "loopowanie" się liczb dziesiętnych.
Dobry ciąg pseudolosowy powinien mieć jak największy okres powtarzalności. Im dłuższy okres
tym trudniej przewidzieć generowane liczby.

Dodatkowo, cytując wykład "wielokrotne wywołanie tych algorytmów z takimi
samymi danymi wejściowymi powoduje wygenerowanie
takich samych wyjściowych ciągów. W przypadku
kluczy kryptograficznych może to okazać się
niebezpieczne, szczególnie, jeżeli kryptoanalityk ma
dostęp do generatora i zna klucz nadrzędny!".

Dodatkowo ciąg pseudolosowy zwykle powinien chaotyczny, nieuporządkowany oraz sprawiający
wrażenie losowego szumu. Np. w teście długiej serii - serię zer albo jedynek
nazywamy długą, jeśli ma długość 26 lub więcej. Test zakończy się sukcesem
jeśli w próbce o długości 20000 bitów nie ma takiej serii. Zatem, mimo, że w przypadku np.
rzutu monetą ciagi losowe '1111111' są równie prawdopodobne co '10001011', to ten
drugi jest bardziej użyteczny przez swoją chaotyczność. Można rzec, że ciągi pseudolosowe
powinny w pewien sposób hołdować paradoksowi hazardzisty.

2.
Jak	testuje	się	losowość ciągów?

3.
Implementacja BBS jest poniżej.

4.
Generacja ciągu 20000 bitów poniżej.

5.
4 testy FIPS 140-2:
 - test pojedynczych bitów
 - test długiej serii
 - test serii
 - test pokerowy

Implementacja poniżej w odpowiednich funkcjacho o adekwatnych nazwach.

6.
Interpretacja wyników: Moje ciągi zdały każdy test za wyjątkiem wszystkich testów serii.
UPDATE: Wynikało to z mojej pomyłki - liczyłem ciągi zer i jedynek razem, a nie osobno.
'''

import random
import sys
import numpy as np
from math import gcd

def generateBBS(x, n, loops, printNumbers = False):
    if printNumbers:
        print('last bit | number')
        print('---------+-----------------------------------------------------------------')

    lastBits = []
    lastBitsStr = ''

    for i in range(0, loops):
        lastBit = x % 2
        if printNumbers:
            print('      ', lastBit, '|', x)
        lastBits.append(lastBit)
        lastBitsStr += str(lastBit)
        x = (x * x) % n

    print('---------------------------------------------------------------------------')

    return lastBits, lastBitsStr

def longSeriesTest(bits, threshold = 26):
    longSeries = []
    currentLength = 1
    previous = None

    for bit in bits:
        if previous == bit:
            currentLength += 1
        else:
            if currentLength >= threshold:
                longSeries.append(currentLength)
            currentLength = 1
        previous = bit

    if currentLength >= threshold:
                longSeries.append(currentLength)

    if threshold == 1:
        return len(longSeries) - 1, longSeries[1:]
    return len(longSeries), longSeries

def pokerTest(bits):
    if len(bits) != 20000:
        print('ERR-00')
        sys.exit()

    quadruples = {}
    for i in range(0, 16):
        binaryQuadruple = [int(x) for x in bin(i)[2:]]
        while len(binaryQuadruple) < 4:
            binaryQuadruple = [0] + binaryQuadruple
        binaryQuadruple = tuple(binaryQuadruple)
        quadruples[binaryQuadruple] = 0

    for i in range(0, len(bits) // 4):
        bit1 = bits[4 * i]
        bit2 = bits[4 * i + 1]
        bit3 = bits[4 * i + 2]
        bit4 = bits[4 * i + 3]
        binaryQuadruple = (bit1, bit2, bit3, bit4)
        quadruples[binaryQuadruple] += 1

    x = 0
    for key in quadruples:
        print(key, ': ', quadruples[key], sep='')
        x += quadruples[key] * quadruples[key]
    x *= 16 / 5000
    x -= 5000
    print('x =', x)
    lower = 2.16
    upper = 46.17
    bounds = [lower, upper, x]
    bounds.sort()
    print(bounds)
    if x > lower and x < upper:
        print('PASSED')
    else:
        print('FAILED')

def singleBitsTest(bits):
    occurences = {0: 0, 1: 0}
    for bit in bits:
        occurences[bit] += 1

    for key in occurences:
        print(key, ': ', occurences[key], sep='')

    lower = 9725
    upper = 10275
    bounds = [lower, upper, occurences[1]]
    bounds.sort()
    print(bounds)
    if occurences[1] > lower and occurences[1] < upper:
        print('PASSED')
    else:
        print('FAILED')

def howManySeries(bits, threshold, digit):
    longSeries = []
    currentLength = 1
    previous = None
    current = None

    for bit in bits:
        current = bit
        if previous == current:
            currentLength += 1
        else:
            if currentLength >= threshold and previous == digit:
                longSeries.append(currentLength)
            currentLength = 1
        previous = current

    if currentLength >= threshold and current == digit:
        longSeries.append(currentLength)

    return len(longSeries), longSeries

def seriesTest(bits):
    series = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}

    bounds = {1: {'lower': 2315, 'upper': 2685},
    2: {'lower': 1114, 'upper': 1386},
    3: {'lower': 527, 'upper': 723},
    4: {'lower': 240, 'upper': 384},
    5: {'lower': 103, 'upper': 209},
    6: {'lower': 103, 'upper': 209}}

    print('0s:')
    for key in series:
        if key != 6:
            series[key] = howManySeries(bits, key, 0)[0] - howManySeries(bits, key + 1, 0)[0]
        if key == 6:
            series[key] = howManySeries(bits, key, 0)[0]
        print(key, ': ', series[key], sep='', end='')
        lower = bounds[key]['lower']
        upper = bounds[key]['upper']
        if series[key] >= lower and series[key] <= upper:
            print(' PASSED')
        else:
            print(' FAILED')

    print('1s:')
    for key in series:
        if key != 6:
            series[key] = howManySeries(bits, key, 1)[0] - howManySeries(bits, key + 1, 1)[0]
        if key == 6:
            series[key] = howManySeries(bits, key, 1)[0]
        print(key, ': ', series[key], sep='', end='')
        lower = bounds[key]['lower']
        upper = bounds[key]['upper']
        if series[key] >= lower and series[key] <= upper:
            print(' PASSED')
        else:
            print(' FAILED')

def main():
    print('---------------------------------------------------------------------------')

    p = 58888239098469463775587912003806191205868774693027
    q = 85604199208400909780924384247288216256224908712067
    #p = 7
    #q = 19

    print('p =', p, 'mod 4 =', p % 4)
    print('q =', q, 'mod 4 =', q % 4)

    n = p * q
    print('n =', n)

    seed = 984661978996588571910503492855159913087256660449473418354928298767417477094308603012085490261513521173459
    #seed = 43
    print('seed =', seed)
    print('gcd(n, seed) = ', gcd(n, seed), sep='')

    x0 = (seed * seed) % n

    lastBits, lastBitsStr = generateBBS(x0, n, 20000)
    print('bits: ', lastBitsStr[:60], '...', sep='')
    print('---------------------------------------------------------------------------')

    #long series test:
    lengths, longSeries = longSeriesTest(lastBits, 26)
    print('lengths of series of 0s or 1s that are longer than 26:', longSeries)
    if lengths == 0:
        print('PASSED')
    else:
        print('FAILED')
    print('---------------------------------------------------------------------------')

    #poker test:
    pokerTest(lastBits)
    print('---------------------------------------------------------------------------')

    #single bits test:
    singleBitsTest(lastBits)
    print('---------------------------------------------------------------------------')

    #series test:
    seriesTest(lastBits)
    print('---------------------------------------------------------------------------')

    #seriesTest([1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0])

if __name__ == '__main__':
    main()