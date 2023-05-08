from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

from DatasetUtils import extractDatasetFromDirectory

x, y, yLabels = extractDatasetFromDirectory("Gestures")
clf = RandomForestClassifier()
clf.fit(x, y)

def getGesture(angles: list):
    current_gesture = -1

    # if angles[1] < 2:
    #     current_gesture = 1
    #
    # if angles[3] < 2:
    #     current_gesture = 2
    #
    # if angles[5] < 2:
    #     current_gesture = 3
    #
    # if angles[9] < 2:
    #     current_gesture = 4

    gesturesProbs = clf.predict_proba([angles])[0]
    current_gesture = gesturesProbs.argmax() if max(gesturesProbs) > 0.75 else -1

    return current_gesture, yLabels[current_gesture]
