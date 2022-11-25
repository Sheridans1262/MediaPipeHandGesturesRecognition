import json
from geometry_extencion import getDistanceBetweenDots
from extencions import Finger, Dot


class KNN:
    def __init__(self, db_filename):
        self.gestures = {}
        self.getGestures(db_filename)
        print(self.getDotsForFinger(Finger.thumb))

    def getGestures(self, db_filename):
        with open(db_filename) as file:
            self.gestures = json.load(file)

    def getDotsForFinger(self, finger: Finger) -> dict:
        result = {}
        finger = str(finger.value)

        for gesture in self.gestures.keys():
            result.update({gesture: self.gestures[gesture][finger]})
        return result

    # def defineGesture(self, palm):
    #     probabilities = []
    #     for finger in palm.fingers():
    #         probabilities.append(self.knnPerFinger(finger))
    #
    #     probabilities.sort()
    #     return list(probabilities)[0]
    #
    # def knnPerFinger(self, finger):
    #     k = 5
    #     distances = {}
    #     for gesture in self.gestures:
    #         for dot in gesture:
    #             distances.update({gesture: getDistanceBetweenDots(dot, finger)})
    #     distances.sort()
    #     return distances[-1:- k - 1:-1]
