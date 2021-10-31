from typing import List
import cv2  # Import openCV
import numpy as np
import math
from random import randint


from numpy.lib.type_check import imag

image = cv2.imread('./hello.png', cv2.IMREAD_UNCHANGED)

b, g, r, a = cv2.split(image)
# Normalizing blue color
b = b/255
b = [[math.floor(item) for item in row] for row in b]


def flatten(List):
    result = []
    for item in List:
        result = result + item
    return result


c0 = [[[0, 1], [0, 1]], [[1, 0], [1, 0]]]
c1 = [[[1, 0], [0, 1]], [[0, 1], [1, 0]]]

part1 = []
part2 = []


def subPixels(pixel):
    radnomNumber = randint(0, 1)
    subpixels1 = c0[radnomNumber][0] if pixel == 0 else c1[radnomNumber][0]
    subpixels2 = c0[radnomNumber][1] if pixel == 0 else c1[radnomNumber][1]
    part1.append(subpixels1)
    part2.append(subpixels2)
    if(radnomNumber == 1):
        return [0, 1]
    return [1, 0]


def chunks(list, chunkLen):
    return [list[i:i+chunkLen] for i in range(len(list))[::chunkLen]]


bresult = list(map(lambda row: [subPixels(pixel) for pixel in row], b))

part1 = chunks(flatten(part1), 2 * len(b[0]))
part2 = chunks(flatten(part2), 2 * len(b[0]))


def merge_parts(List1, List2):
    resultList = [[0 for _ in range(len(List1))] for _ in range(len(List1))]
    for rowIndex in range(len(List1)):
        for columnIndex in range(0, len(List1[rowIndex]), 2):
            firstPixelofFirstList = List1[rowIndex][columnIndex]
            secondPixelofFirstList = List1[rowIndex][columnIndex + 1]
            firstPixelofSecondList = List2[rowIndex][columnIndex]
            secondPixelofSecondList = List2[rowIndex][columnIndex + 1]
            calculation = firstPixelofFirstList or firstPixelofSecondList + \
                secondPixelofFirstList or secondPixelofSecondList
            resultList[rowIndex][math.floor(columnIndex/2)] = calculation
    return resultList


mergedList = merge_parts(part1, part2)
mergedList = list(map(lambda row: [(0 if pixel != 2 else 2)
                                   for pixel in row], mergedList))
np.shape(mergedList)


bresult = np.float64(bresult)
bfinal = np.float64(mergedList)
part1 = np.float64(part1)
part2 = np.float64(part2)

cv2.imshow("Part1", part1)
cv2.imshow("Part2", part2)
cv2.imshow("Merged", bfinal)

cv2.waitKey(0)
