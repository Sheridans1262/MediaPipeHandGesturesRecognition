from math import sqrt

from mediapipe_hands import MediapipeHands
from plane import Plane
from extencions import Dot
import time
from knn_algorithm import KNN



def main():
    mediapipeTest()

def mediapipeTest():
    mpipe = MediapipeHands()
    # mpipe.processHandsFromVideo()
    mpipe.processHandsFromImage("Images/test1.jpg")
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

    # pl = Plane(W, I, P)
    # print(pl.dotProjectionOnLine(Dot(0, 1, -1), 2, 3, -6, -4, 1, 1))
    # print(pl.getDotProjectionOnLine(Dot(0, 1, -1), Dot(2, -3, 0), Dot(1, -3, -5)))
    # KNN.defineGesture(Dot(7, 3, 5), "index")
    # start = time.perf_counter()
    # knn = KNN("db.json")
    # print(f"Time: {time.perf_counter() - start} sec")

if __name__ == '__main__':
    main()
