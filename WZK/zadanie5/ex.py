import random
import sys
import numpy as np
from math import gcd
import bitarray
from bitarray.util import ba2int

class PublicKey:
    e = 0
    n = 0

class PrivateKey:
    d = 0
    n = 0

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def modInverse(a, m):
    g = gcd(a, m)
    if (g != 1):
        print("Inverse doesn't exist")
        return None
    else:
        return pow(a, m - 2, m)

def encode(message, publicKey, display = True):
    messageBits = bitarray.bitarray()
    messageBits.frombytes(message.encode('utf-8'))
    if display:
        print('message as bits:', messageBits)
        print('---------------------------------------------------------------------------')

    messageInt = ba2int(messageBits)
    if display:
        print('message as int:', messageInt)
        print('---------------------------------------------------------------------------')

    encodedMessage = pow(messageInt, publicKey.e, publicKey.n)
    return encodedMessage

def decode(encodedMessage, privateKey, display = True):
    decodedMessageInt = pow(encodedMessage, privateKey.d, privateKey.n)
    if display:
        print('decoded message as int:', decodedMessageInt)
        print('---------------------------------------------------------------------------')

    decodedMessage = chr(decodedMessageInt)
    if display:
        print('decoded message as char:', decodedMessage)
        print('---------------------------------------------------------------------------')

    return decodedMessage

def main():
    print('---------------------------------------------------------------------------')

    p = 440652540385366476885648349606092631044387368497923129947867 #60
    q = 848678487181295759680383727940935479949828086390833874248117 #60
    #p = 4751 #4
    #q = 9007 #4
    print('p =', p)
    print('q =', q)

    n = p * q
    print('n =', n)

    phi = (p - 1) * (q - 1)
    print('phi =', phi)

    e = 331217644374414450300103554646128062125802050357921772483749 #60
    #e = 9421 #4
    print('e =', e)
    print('gcd(phi, e) =', gcd(phi, e))

    '''
    (e * d - 1) mod phi = 0 <===> e * d - 1 = x * phi <===> d = (x * phi + 1) / e
    '''

    #x = 2
    #notFound = True

    #print('---------------------------------------------------------------------------')
    #pierwsza metoda do wyznaczania d (brute force):
    #print('searching for x...')
    '''
    while notFound:
        if x % 1000 == 0:
            pass
            #print(x)
        numerator = x * phi + 1
        if numerator % e == 0:
            d = numerator // e
            notFound = False
        else:
            x += 1
    '''

    #druga metoda, korzystająca z odwrotności modulo:
    d = pow(e, -1, phi)

    #print('x =', x)
    #print('d = (x * phi + 1) / e')
    #print('d = (', x, ' * ', phi, ' + 1) / ', e, sep='')
    print('d =', d) 
    print('(e * d - 1) mod phi =', (e * d - 1) % phi)

    print('---------------------------------------------------------------------------')

    publicKey = PublicKey()
    publicKey.e = e
    publicKey.n = n

    privateKey = PrivateKey()
    privateKey.d = d
    privateKey.n = n

    message = 'Ja kocham Wybrane Zagadnienia Kryptograficzne! :-)'
    print('message: "', message, '" of length ', len(message), sep='')
    print('---------------------------------------------------------------------------')

    encodedMessage = [encode(character, publicKey, False) for character in message]
    print('encoded message characters:', encodedMessage)
    print('---------------------------------------------------------------------------')

    decodedMessage = ''.join([decode(character, privateKey, False) for character in encodedMessage])
    print('decoded message: "', decodedMessage, '" of length ', len(decodedMessage), sep='')
    print('---------------------------------------------------------------------------')

    if decodedMessage == message:
        print('MESSAGES MATCH!')
    else:
        print('MESSAGES DON`T MATCH!')

if __name__ == '__main__':
    main()