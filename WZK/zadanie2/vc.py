import random
import sys
import numpy as np
from PIL import Image

class Matrices:
    def __init__(self):
        self.C0 = self.white = {0: {'share1': [0, 1], 'share2': [0, 1]}, 1: {'share1': [1, 0], 'share2': [1, 0]}}
        self.C1 = self.black = {0: {'share1': [1, 0], 'share2': [0, 1]}, 1: {'share1': [0, 1], 'share2': [1, 0]}}
        self.C0RGB = self.whiteRGB = {0: {'share1': [(255, 255, 255), (0, 0, 0)], 'share2': [(255, 255, 255), (0, 0, 0)]}, 1: {'share1': [(0, 0, 0), (255, 255, 255)], 'share2': [(0, 0, 0), (255, 255, 255)]}}
        self.C1RGB = self.blackRGB = {0: {'share1': [(0, 0, 0), (255, 255, 255)], 'share2': [(255, 255, 255), (0, 0, 0)]}, 1: {'share1': [(255, 255, 255), (0, 0, 0)], 'share2': [(0, 0, 0), (255, 255, 255)]}}

    def getShares(self, color):
        if color == 'white' or color == 'C0' or color == 0 or color == (255, 255, 255):
            return self.white[random.randrange(0, 2)]
        elif color == 'black' or color == 'C1' or color == 1 or color == (0, 0, 0):
            return self.black[random.randrange(0, 2)]
        else:
            print('ERROR #00')
            return None

    def getSharesRGB(self, color):
        if color == 'white' or color == 'C0' or color == 0 or color == (255, 255, 255):
            return self.whiteRGB[random.randrange(0, 2)]
        elif color == 'black' or color == 'C1' or color == 1 or color == (0, 0, 0):
            return self.blackRGB[random.randrange(0, 2)]
        else:
            #print('ERROR #00:', color)
            return None

def code():
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    MATRICES = Matrices()
    TRESHOLD = 300

    imageName = sys.argv[2]
    image = Image.open(imageName)
    image = image.convert('RGB')
    image.show()
    #image.show()
    imageWidth, imageHeight = image.size
    print('image is', imageWidth, '*', imageHeight, 'pixels')

    imagePixels = image.load()

    share1 = Image.new('RGB', (imageWidth * 2, imageHeight * 2))
    share1Pixels = share1.load()
    #share1.setflags(write=1)
    #share1 = np.asarray(share1, dtype=np.uint8)
    share2 = Image.new('RGB', (imageWidth * 2, imageHeight * 2))
    share2Pixels = share2.load()
    #share2.setflags(write=1)
    #share2 = np.asarray(share2, dtype=np.uint8)

    for x in range(0, imageWidth):
        for y in range(0, imageHeight):
            pixelRGB = imagePixels[x, y]
            shares = MATRICES.getSharesRGB(pixelRGB)

            if shares == None:
                #print('ERROR #02')
                pixelSum = pixelRGB[0] + pixelRGB[1] + pixelRGB[2]
                #if pixelSum > 382:
                if pixelSum > TRESHOLD:
                    shares = MATRICES.getSharesRGB(WHITE)
                else:
                    shares = MATRICES.getSharesRGB(BLACK)

            x1 = x * 2
            x2 = x * 2 + 1
            y1 = y * 2
            y2 = y * 2 + 1

            share1Pixels[x1, y1] = shares['share1'][0]
            share1Pixels[x2, y1] = shares['share1'][1]
            share1Pixels[x1, y2] = shares['share1'][0]
            share1Pixels[x2, y2] = shares['share1'][1]

            share2Pixels[x1, y1] = shares['share2'][0]
            share2Pixels[x2, y1] = shares['share2'][1]
            share2Pixels[x1, y2] = shares['share2'][0]
            share2Pixels[x2, y2] = shares['share2'][1]

    #share1.show()
    #share2.show()
    share1.save('share1.png')
    share2.save('share2.png')

def decode():
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    share1Name = sys.argv[2]
    share2Name = sys.argv[3]
    share1 = Image.open(share1Name)
    share1 = share1.convert('RGB')
    share2 = Image.open(share2Name)
    share2 = share2.convert('RGB')

    share1Pixels = share1.load()
    share2Pixels = share2.load()

    if share1.size != share2.size:
        print('ERROR #03')
    imageWidth, imageHeight = share1.size

    image = Image.new('RGB', (imageWidth, imageHeight))
    imagePixels = image.load()

    for x in range(0, imageWidth):
        for y in range(0, imageHeight):
            if (share1Pixels[x, y] != WHITE and share1Pixels[x, y] != BLACK) or (share2Pixels[x, y] != WHITE and share2Pixels[x, y] != BLACK):
                print('ERROR #04')
                sys.exit()
            if share1Pixels[x, y] == WHITE and share2Pixels[x, y] == WHITE:
                imagePixels[x, y] = WHITE
            else:
                imagePixels[x, y] = BLACK

    image.show()

def main():
    #matrices = Matrices()
    #print(matrices.getShares('white'))
    #print(matrices.getShares('black'))

    function = sys.argv[1]
    if function == 'code':
        code()
    elif function == 'decode':
        decode()
    else:
        print('ERROR #01')

if __name__ == '__main__':
    main()