import cv2
import mediapipe as mp
import time
from os import listdir
from os.path import isfile, join

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

from AnglesExtencion import getAngles


def createDatasetForGesture(gestureName: str):
    cam = cv2.VideoCapture(0)

    mpHands = mp.solutions.hands
    hands = mpHands.Hands(max_num_hands=1)
    mpDraw = mp.solutions.drawing_utils

    gesturesResults = []

    landmarksRaw = []

    startTime = time.time()
    while True:
        _, img = cam.read()

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(imgRGB)

        if results.multi_hand_landmarks:
            for handLandmarks in results.multi_hand_landmarks:
                landmarksRaw.append(handLandmarks)
                mpDraw.draw_landmarks(img, handLandmarks, mpHands.HAND_CONNECTIONS)

        img = cv2.flip(img, 1)
        cv2.imshow("Cam", img)
        if cv2.waitKey(1) == ord('q'):
            break

    print(f"{time.time() - startTime} seconds")
    print(f"{len(landmarksRaw)} datarows")
    # print(landmarksRaw)
    for handLandmarks in landmarksRaw:
        angles = getAngles(handLandmarks)
        gesturesResults.append(angles)

    # print(gesturesResults)
    with open(f"Gestures/{gestureName}.txt", 'a') as file:
        for line in gesturesResults:
            for node in line:
                file.write(str(node) + ' ')
            file.write('\n')


def extractDatasetFromDirectory(datasetPath: str):
    directoryFiles = [file for file in listdir(datasetPath) if isfile(join(datasetPath, file))]

    yLabels = {-1: "Unknown gesture"}

    x = []
    y = []
    for index, fileName in enumerate(directoryFiles):
        gestureName = ' '.join(fileName.split('.')[:-1])
        yLabels.update({index: gestureName})

        with open(f"{datasetPath}/{fileName}", 'r') as file:
            while True:
                dataRow = file.readline()
                if len(dataRow) == 0:
                    break

                processedDataRow = [float(dataNode) for dataNode in dataRow.split(' ')[0:-1]]
                x.append(processedDataRow)
                y.append(index)

    print(len(x))
    # print(x)
    # print(len(y))
    # print(y)
    # print(len(yLabels))
    # print(yLabels)

    return x, y, yLabels

# createDatasetForGesture("Fist")
# extractDatasetFromDirectory("Gestures")
# x, y, yLabels = extractDatasetFromDirectory("Gestures")
# xTrain, xTest, yTrain, yTest = train_test_split(x, y, test_size=0.2)
#
# clf = RandomForestClassifier()
# clf.fit(xTrain, yTrain)
#
# print(clf.predict_proba([xTest[-5]]))
# print(yTest[-5])
