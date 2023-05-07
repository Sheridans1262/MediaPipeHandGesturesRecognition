import cv2
import mediapipe as mp
import time
from os import listdir
from os.path import isfile, join

from dots_normalization import getAngles


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

    dataset = {}
    for fileName in directoryFiles:
        gestureData = []

        with open(f"{datasetPath}/{fileName}", 'r') as file:
            while True:
                dataRow = file.readline()
                if len(dataRow) == 0:
                    break

                processedDataRow = [float(dataNode) for dataNode in dataRow.split(' ')[0:-1]]
                gestureData.append(processedDataRow)

        gestureName = ' '.join(fileName.split('.')[:-1])

        dataset.update({gestureName: gestureData})

    return dataset


# createDatasetForGesture("FlatPalm")
extractDatasetFromDirectory("Gestures")
