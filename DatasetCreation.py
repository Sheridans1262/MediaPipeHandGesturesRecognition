import cv2
import mediapipe as mp
import time

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
                # landmarks = []
                # for id, landmark in enumerate(handLandmarks.landmark):
                #     print(id, landmark)
                #     landmarks.append(landmark)

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
        # file.writelines(gesturesResults)


createDatasetForGesture("PointingIndexFinger")
