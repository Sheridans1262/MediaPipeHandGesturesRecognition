import json
from geometry_extencion import getDistanceBetweenDots
from gesture import Gesture

class KNN:
    def __init__(self, db_filename):
        self.gestures = {}
        self.getGestures(db_filename)

    def getGestures(self, db_filename):
        with open(db_filename) as file:
            self.gestures = json.load(file)

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
