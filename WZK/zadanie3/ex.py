import random
import sys
import numpy as np
from PIL import Image

def bin(s):
    return str(s) if s<=1 else bin(s >> 1) + str(s & 1)

def code():
    #pixels required to code one character assuming they use 1 bit per RGB value
    #so - 'X' requires 8 bits, that's 8 RGB values, but they come in threes, so 
    #1 character requires ceil(8 / 3) pixels:
    CHARACTER_SIZE = 3

    STOPPER = '$'

    #name of the txt file with secret text:
    secretFileName = sys.argv[3]
    secret = ''
    with open(secretFileName, 'r') as secretFile:
        secret = secretFile.read().rstrip()

    #add $ to signify ending of coded message:
    secret += STOPPER

    #length of the secret:
    secretLength = len(secret)
    print('secret: "', secret[:-1], '" of length ', secretLength - 1, '', sep='')

    #image to encrypt the secret:
    imageName = sys.argv[2]
    image = Image.open(imageName)
    image = image.convert('RGB')
    #image.show()
    imageWidth, imageHeight = image.size
    print('image is', imageWidth, '*', imageHeight, 'pixels')
    print('that is maximally', imageWidth * imageHeight // 3, 'characters available')

    imagePixels = image.load()

    #loop coding all the pixels:
    charactersCoded = 0
    #y is vertical position:
    for y in range(0, imageHeight):
        #x is horizontal position:
        for x in range(0, imageWidth, CHARACTER_SIZE):
            #if there is no sufficient space left in current row:
            if x + 2 >= imageWidth:
                continue

            #list of pixels (3 pixels as RGB tuples) that will code one character:
            pixels = []
            for i in range(0, CHARACTER_SIZE):
                pixel = imagePixels[x + i, y]
                pixels.append(pixel)
            #print(pixels)
            #sys.exit()

            #character to code:
            character = secret[charactersCoded]
            extra = ''
            if character == STOPPER:
                extra = '(stopper)'
            print('coding |', character, '| ', charactersCoded + 1, '. ', extra, sep='')
            charactersCoded += 1

            characterInt = ord(character)
            #print(characterInt)

            characterBits = bin(characterInt)
            characterBitsLength = len(characterBits)
            for i in range(0, CHARACTER_SIZE * 3 - characterBitsLength):
                characterBits = '0' + characterBits
            #print(characterBits)
            characterBitsLength = len(characterBits)
            
            bitsCoded = 0
            pixelsModified = []
            for pixel in pixels:
                #print(pixel)
                r = pixel[0]
                g = pixel[1]
                b = pixel[2]
                #print(r, g, b)

                rBits = bin(r)
                gBits = bin(g)
                bBits = bin(b)
                #print(rBits, gBits, bBits)

                rBits = rBits[:-1] + characterBits[bitsCoded]
                bitsCoded += 1
                gBits = gBits[:-1] + characterBits[bitsCoded]
                bitsCoded += 1
                bBits = bBits[:-1] + characterBits[bitsCoded]
                bitsCoded += 1
                #print(rBits, gBits, bBits)

                r = int(rBits, 2)
                g = int(gBits, 2)
                b = int(bBits, 2)
                #print(r, g, b)

                pixelsModified.append((r, g, b))

            #changing original pixels:
            for i in range(0, CHARACTER_SIZE):
                imagePixels[x + i, y] = pixelsModified[i]

            #saving if done:
            if charactersCoded == secretLength:
                image.save('encrypted.png')
                return

def decode():
    CHARACTER_SIZE = 3

    STOPPER = '$'

    secret = ''

    imageName = sys.argv[2]
    image = Image.open(imageName)
    image = image.convert('RGB')
    #image.show()
    imageWidth, imageHeight = image.size
    print('image is', imageWidth, '*', imageHeight, 'pixels')
    print('that is maximally', imageWidth * imageHeight // 3, 'characters available')

    imagePixels = image.load()

    for y in range(0, imageHeight):
        for x in range(0, imageWidth, CHARACTER_SIZE):
            if x + 2 >= imageWidth:
                continue

            #list of pixels (3 pixels as RGB tuples) that will code one character:
            pixels = []
            for i in range(0, CHARACTER_SIZE):
                pixel = imagePixels[x + i, y]
                pixels.append(pixel)
            
            pixelsLastBits = ''
            for pixel in pixels:
                r = pixel[0]
                g = pixel[1]
                b = pixel[2]

                rBits = bin(r)
                gBits = bin(g)
                bBits = bin(b)

                #print(rBits, gBits, bBits)
                rLastBit = rBits[-1]
                gLastBit = gBits[-1]
                bLastBit = bBits[-1]
                #print(rLastBit, gLastBit, bLastBit)

                pixelsLastBits += rLastBit
                pixelsLastBits += gLastBit
                pixelsLastBits += bLastBit

            characterInt = int(pixelsLastBits, 2)
            character = chr(characterInt)
            print('decoded |', character, '|', sep='')
            if character != STOPPER:
                secret += character
            else:
                print('secret should be: "', secret, '"', sep='')
                return

def check():
    image1Name = sys.argv[2]
    image2Name = sys.argv[3]
    image1 = Image.open(image1Name)
    image1 = image1.convert('RGB')
    image2 = Image.open(image2Name)
    image2 = image2.convert('RGB')
    #image.show()
    image1Width, image1Height = image1.size
    image2Width, image2Height = image2.size

    if image1.size != image2.size:
        print('IMAGES ARE NOT THE SAME')

    image1Pixels = image1.load()
    image2Pixels = image2.load()

    for x in range(0, image1Width):
        for y in range(0, image1Height):
            if image1Pixels[x, y] != image2Pixels[x, y]:
                print('IMAGES ARE NOT THE SAME! FIRST DIFFERENCE AT [', x, ', ', y, ']', sep='')
                return

    print('IMAGES ARE IDENTICAL')

def main():
    function = sys.argv[1]
    if function == 'code':
        code()
    elif function == 'decode':
        decode()
    elif function == 'check':
        check()
    else:
        print('ERROR #00')

if __name__ == '__main__':
    main()