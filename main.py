from math import sqrt

from mediapipe_hands import MediapipeHands
from plane import Plane, Dot
import time


def main():
    mediapipeTest()

def lengthAndAngle():
    ...

def twoLengths():
    ...

def mediapipeTest():
    mpipe = MediapipeHands()
    mpipe.processHandsFromVideo()
    # mpipe.processHandsFromImage("Images/one finger palm faced.jpg")
    # mpipe.processHandsFromImage("Images/two fingers palm away.jpg")

    # W = Dot(7, 3, 5)
    # I = Dot(4, 0, -1)
    # P = Dot(1, 1, -2)
    # A = Dot(9, 10, 7)
    #
    # start = time.perf_counter()
    # for i in range(20):
    #     math.sqrt((i + 1)**2 + (i + 2)**2 + (i + 3)**2)
    #     pl = Plane(W, I, P)
    #     A_proj = pl.getDotProjectionOnPlane(A)
    # print(1/(time.perf_counter() - start), " sec")


if __name__ == '__main__':
    main()
